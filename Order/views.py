import json
import time
from rest_framework import generics
from Order.serializers import *
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView

from Order.models import *
from blog.models import *

# ? sandbox merchant
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

amount = 1000  # Rial / Required
description = "نهایی کردن خرید شما از سایت ما"  # Required
phone = ''  # Optional

CallbackURL = 'http://127.0.0.1:8000/Order/verify-payment/'


def add_product_to_order(request: HttpRequest):
    product_id = int(request.GET.get('product_id'))
    count = int(request.GET.get('count'))
    if count < 1:
        return JsonResponse({
            'status': 'invalid_count'
        })
    if request.user.is_authenticated:
        product = Product.objects.filter(pk=product_id).first()
        if product is not None:
            current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
            current_order_detail = current_order.orderdetail_set.filter(product_id=product_id).first()

            if current_order_detail is not None:
                current_order_detail.count += int(count)
                current_order_detail.save()
            else:
                new_detail = OrderDetail(order_id=current_order.id, product_id=product_id,
                                         final_price=product.price * count, count=count)
                new_detail.save()
            return JsonResponse({
                'status': 'success'
            })

        else:
            return JsonResponse({
                'status': 'not_found'
            })
    else:
        return JsonResponse({
            'status': 'not_authenticated'
        })


def remove_from_cart(request: HttpRequest):
    product_id = int(request.GET.get('product_id'))

    cart_item = OrderDetail.objects.filter(product_id=product_id).first()
    print(cart_item)
    if cart_item.count > 1:
        cart_item.count -= 1
        cart_item.save()
    else:
        cart_item.delete()

    total_price = cart_item.final_price * int(cart_item.count)
    return JsonResponse({
        'final_price': total_price
    })


def add_from_cart(request: HttpRequest):
    product_id = int(request.GET.get('product_id'))
    cart_item = OrderDetail.objects.filter(product_id=product_id).first()
    print(cart_item)
    if cart_item.count >= 1:
        cart_item.count += 1
        cart_item.save()

    total_price = cart_item.final_price * int(cart_item.count)
    return JsonResponse({
        'final_price': total_price
    })


@login_required
def request_payment(request: HttpRequest):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    final_price = current_order.calculate_total()
    if final_price == 0:
        return redirect(reverse('blog:index'))

    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": int(final_price / 10),
        "Description": description,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data

    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                return redirect(ZP_API_STARTPAY + str(response['Authority']))
            else:
                return JsonResponse({'status': 'pay error'})
        else:
            return JsonResponse({'status': 'pay error'})

    except requests.exceptions.Timeout:
        return JsonResponse({'status': 'pay error'})
    except requests.exceptions.ConnectionError:
        return JsonResponse({'status': 'pay error'})


def verify_payment(request: HttpRequest):
    try:
        current_order = Order.objects.get(is_paid=False, user_id=request.user.id)
    except:
        return redirect('blog:index')
    total_price = current_order.calculate_total_price()
    if total_price == 0:
        return redirect(reverse('blog:index'))

    for order in current_order.orderdetail_set.all():
        if order.product.order_count is not None:
            order.product.order_count = int(order.product.order_count) + order.count
        else:
            order.product.order_count = order.count


    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": int(total_price * 10),
        "Authority": request.GET.get('Authority'),
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

    if response.status_code == 200:
        response = response.json()
        current_order.is_paid = True
        current_order.save()
        if response['Status'] == 100:
            return render(request, 'payment_result.html',
                          {'success': f'تراکنش با موفقیت انجام شد'})
        else:
            return render(request, 'payment_result.html',{'error': 'error'})
    else:
        return JsonResponse({'status': 'nop'})


class CheckoutView(View):
    template_name = 'checkout.html'
    def get(self, request, *args, **kwargs):
        current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
        total_price = current_order.calculate_total_price()
        final_price = current_order.calculate_total()


        if total_price == 0:
            return redirect(reverse('blog:index'))
        user = User.objects.get(id=request.user.id)
        orders = OrderDetail.objects.filter(order = current_order)

        context = {
            'media_url': settings.MEDIA_URL,
            'user': user,
            'orders': orders,
            'total_price': total_price,
            'final_price': final_price,

        }
        return render(request, self.template_name,context)
    def post(self, request, *args, **kwargs):
        current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
        current_order.is_paid = True
        current_order.save()
        current_order.orderdetail_set.all().delete()
        return render(request, self.template_name)


class Order_api(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetail_api(generics.ListCreateAPIView):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer


