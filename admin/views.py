import decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic import View, DetailView
from account_shop_project.models import *
from blog.models import *
from comment.models import *
from Order.models import *
from admin.forms import *


def media_admin(request):
    return {'media_url': settings.MEDIA_URL, }


class PanelView(View):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        products = Product.objects.all()
        orders = Order.objects.filter(is_paid=True, user=request.user)

        time_sort = products.order_by('-created_time')[:10]
        products_sell = products.order_by('-order_count')[:10]
        comment = Comment.objects.all()
        rating = Rating.objects.all()
        product_count = 0
        return_count = 0
        comment_count = 0
        for _ in products:
            product_count += 1
        for _ in comment:
            comment_count += 1
        for order in orders:
            if order.status == 'Returned':
                return_count += 1
        sell_count = 0
        for _ in orders:
            sell_count += 1

        sell_price = 0
        for order in orders:
            sell_price += order.calculate_total_price()
        context = {
            'media_url': settings.MEDIA_URL,
            'user': user,
            'time_sort': time_sort,
            'products_sell': products_sell,
            'comment': comment,
            'rating': rating,
            'product_count': product_count,
            'return_count': return_count,
            'comment_count': comment_count,
            'sell_count': sell_count,
            'sell_price': sell_price

        }
        return render(request, 'admin/Panel.html', context)


class ProductView(View):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)

        product_filter = request.GET.get('filter')

        if product_filter == '1':
            products = Product.objects.all().order_by('order_count')

        elif product_filter == '2':
            products = Product.objects.all().order_by('price')

        elif product_filter == '3':
            products = Product.objects.all().order_by('-discount')

        else:
            products = Product.objects.all()

        product_count = 0
        rate_count = 0
        comment_count = 0
        for _ in products:
            product_count += 1

        query = request.GET.get('q')

        if query:
            products = Product.objects.filter(title__icontains=query)

        context = {
            'media_url': settings.MEDIA_URL,
            'user': user,
            'product_count': product_count,
            'rate_count': rate_count,
            'comment_count': comment_count,
            'products': products

        }

        return render(request, 'admin/post-catalogs.html', context)


class EditProductView(View):
    def get(self, request, product_id):
        user = User.objects.get(id=request.user.id)
        product = Product.objects.filter(id=product_id).first()
        category = Category.objects.all()

        context = {
            'media_url': settings.MEDIA_URL,
            'user': user,
            'product': product,
            'category': category,

        }
        return render(request, 'admin/editProduct.html', context)

    def post(self, request, product_id):
        product_title = request.POST.get('product_title')
        product_price = decimal.Decimal(request.POST.get('product_price'))
        product_image = request.FILES.get('product_image')
        product_date = request.POST.get('product_date')
        product_discount = int(request.POST.get('product_discount'))
        product_order_count = request.POST.get('product_order_count')
        product_visit_count = request.POST.get('product_visit_count')
        product_category = request.POST.get('product_category')

        product = Product.objects.get(id=product_id)
        product.title = product_title
        product.category = int(product_category)
        product.price = product_price
        product.image = product_image
        product.discount = product_discount
        product.date = product_date
        product.visit_count = product_visit_count
        product.order_count = product_order_count
        product.save()

        return redirect('panel:products')

    def post(self, request: HttpRequest, product_id):
        product_title = request.POST.get('product_title')
        product_price = decimal.Decimal(request.POST.get('product_price'))
        product_image = request.FILES.get('product_image')
        product_date = request.POST.get('product_date')
        product_discount = int(request.POST.get('product_discount'))
        product_order_count = request.POST.get('product_order_count')
        product_visit_count = request.POST.get('product_visit_count')
        product_category = request.POST.get('product_category')

        product = Product.objects.get(id=product_id)

        product.title = product_title
        product.price = decimal.Decimal(product_price)
        product.created_time = product_date
        product.discount = product_discount
        product.order_count = product_order_count
        product.visited_count = product_visit_count
        if product_image != None:
            product.image = product_image
        cat = Category.objects.get(id=int(product_category))
        product.category_id = int(product_category)
        product.save()
        return render(request, 'admin/editProduct.html')


class AddProductView(View):
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        category = Category.objects.all()
        context = {
            'media_url': settings.MEDIA_URL,
            'user': user,
            'category': category

        }
        return render(request, 'admin/addProduct.html', context)

    def post(self, request: HttpRequest):
        product_title = request.POST.get('product_title')
        product_price = decimal.Decimal(request.POST.get('product_price'))
        product_image = request.FILES.get('product_image')
        product_date = request.POST.get('product_date')
        product_discount = int(request.POST.get('product_discount'))
        product_order_count = request.POST.get('product_order_count')
        product_visit_count = request.POST.get('product_visit_count')
        product_category = request.POST.get('product_category')

        Product.objects.create(category_id=int(product_category), title=product_title,
                               price=product_price, image=product_image,
                               discount=product_discount, created_time=product_date,
                               order_count=product_order_count, visited_count=product_visit_count)

        return render(request, 'admin/addProduct.html')


def delete_product(request: HttpRequest, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    return JsonResponse({'message': 'با موفقیت حذف شد!'})


class InvoiceView(View):
    def get(self, request, *args, **kwargs):
        invoice_filter = request.GET.get('filter')

        queryset = Order.objects.all().order_by('payment_date')
        final_price = 0  #
        if queryset.exists():
            for order in queryset:
                final_price += order.calculate_total()

        context = {
            'media_url': settings.MEDIA_URL,
            'object_list': queryset,
            'final_price': final_price,

        }
        return render(request, 'admin/factorAdmin.html', context)


def invoice_delete(request, invoice_id):
    invoice = Order.objects.get(id=invoice_id)
    invoice.delete()

    return JsonResponse({'message': 'با موفقیت حذف شد!'})


def invoice_item_delete(request, invoice_id):
    order = OrderDetail.objects.get(id=invoice_id)
    order.delete()
    return JsonResponse({'message': 'با موفقیت حذف شد!'})


def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return JsonResponse({'message': 'با موفقیت حذف شد!'})


class InvoiceDetailView(View):
    def get(self, request):
        order = OrderDetail.objects.all()
        context = {
            'media_url': settings.MEDIA_URL,
            'order': order
        }
        return render(request, 'admin/invoice_item.html', context)


class EditInvoiceView(View):
    def get(self, request, invoice_id):
        orders = Order.objects.all()
        user = request.user.id
        users = User.objects.all()
        order = Order.objects.get(id=invoice_id)
        context = {
            'media_url': settings.MEDIA_URL,
            'order': order,
            'orders': orders,
            'users': users,
            'user': user
        }
        return render(request, 'admin/editInvoice.html', context)

    def post(self, request, invoice_id):
        # انجام عملیات مورد نیاز
        order = Order.objects.get(id=invoice_id)
        invoice_user = request.POST.get('invoice_user')
        invoice_status = request.POST.get('invoice_status')
        invoice_is_paid = request.POST.get('invoice_is_paid')

        order.user_id = int(invoice_user)
        order.is_paid = invoice_is_paid.capitalize()
        order.status = invoice_status
        order.save()

        return redirect('panel:invoice')


class AddInvoiceView(View):
    def get(self, request):
        user = request.user.id
        users = User.objects.all()

        context = {
            'media_url': settings.MEDIA_URL,

            'users': users,
            'user': user
        }
        return render(request, 'admin/addInvoice.html', context)

    def post(self, request):
        # انجام عملیات مورد نیاز

        invoice_user = request.POST.get('invoice_user')
        invoice_is_paid = request.POST.get('invoice_is_paid')

        Order.objects.create(user_id=int(invoice_user), is_paid=invoice_is_paid.capitalize())

        return redirect('panel:invoice')


class AddInvoiceDetailView(View):
    def get(self, request, ):
        order = OrderDetail.objects.all()
        product = Product.objects.all()
        order_user = Order.objects.all()
        context = {
            'media_url': settings.MEDIA_URL,
            'order': order,
            'product': product,
            'order_user': order_user
        }
        return render(request, 'admin/add_invoice_item.html', context)

    def post(self, request):
        invoice_item_user = request.POST.get('order_user')
        invoice_item_product = request.POST.get('order_product')
        invoice_item_final_price = request.POST.get('order_final_price')
        invoice_item_count = request.POST.get('order_count')

        OrderDetail.objects.create(
            product_id=int(invoice_item_product),
            order_id=int(invoice_item_user),
            final_price=invoice_item_final_price,
            count=invoice_item_count

        )
        return redirect('panel:invoice_admin_detail')


class EditInvoiceDetailView(View):
    def get(self, request, invoice_id):
        order_item = OrderDetail.objects.get(id=invoice_id)
        product = Product.objects.all()
        order_user = Order.objects.all()

        context = {
            'media_url': settings.MEDIA_URL,
            'order_item': order_item,
            'product': product,
            'order_user': order_user
        }
        return render(request, 'admin/edit_invoice_item.html', context)

    def post(self, request, invoice_id):
        invoice_item_user = request.POST.get('order_user')
        invoice_item_product = request.POST.get('order_product')
        invoice_item_final_price = request.POST.get('order_final_price')
        invoice_item_count = request.POST.get('order_count')

        order = OrderDetail.objects.get(id=invoice_id)
        order.product_id = int(invoice_item_product)
        order.order_id = int(invoice_item_user)
        order.final_price = invoice_item_final_price
        order.count = invoice_item_count
        order.save()

        return redirect('panel:invoice_admin_detail')


class FactorFilter(View):
    def get(self, request):
        order = Order.objects.filter(is_paid=True)
        form = FactorForm()
        context = {
            'media_url': settings.MEDIA_URL,
            'object_list': order,
            'form': form
        }
        return render(request, 'admin/factor_filter.html', context)

    def post(self, request):
        form = FactorForm(request.POST)
        if form.is_valid():
            filter_start = form.cleaned_data['start_date']
            filter_end = form.cleaned_data['end_date']
            if filter_start and filter_end:
                order = Order.objects.filter(payment_date__range=[filter_start, filter_end], is_paid=True)

            elif filter_start:
                order = Order.objects.filter(payment_date__gte=filter_start, is_paid=True)
            elif filter_end:
                order = Order.objects.filter(payment_date__lte=filter_end, is_paid=True)
            else:
                order = Order.objects.filter(is_paid=True)
        else:
            order = Order.objects.filter(is_paid=True)

        context = {
            'media_url': settings.MEDIA_URL,
            'object_list': order,
            'form': form
        }
        return render(request, 'admin/factor_filter.html', context)
