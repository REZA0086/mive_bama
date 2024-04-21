from django.conf import settings
from django.contrib.auth import login
from django.db.models import Sum, Avg
from django.http import Http404, HttpRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views.generic import View
from Order.models import *
from blog.models import *
from blog.forms import *

from comment.models import *
from comment.forms import *
from rest_framework import generics
from blog.serializers import *


def media_admin(request):
    return {'media_url': settings.MEDIA_URL, }


class IndexView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        category = request.GET.get('category')
        products_category = Product.objects.filter(category=category)

        category = Category.objects.all()

        try:
            user = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            user = None
        current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
        total_amount = sum(item.Final_Price() for item in current_order.orderdetail_set.all())
        orders = OrderDetail.objects.filter(order=current_order)
        count_order = 0
        for _ in orders:
            count_order += 1
        products = Product.objects.all()
        cheapest_products = products.order_by('price')[:10]
        time_sort = products.order_by('-created_time')[:10]
        products_discount = products.order_by('-discount')[:10]

        products_sell = products.order_by('order_count')[:10]

        header_index = HeaderIndex.objects.all().first()
        title_index = TitleIndex.objects.all().first()
        slider_index = SliderIndex.objects.all()
        image_index = ImageIndex.objects.all()
        advantage_index = Advantage.objects.all()
        footer = Footer.objects.all().first()

        context = {
            'media_url': settings.MEDIA_URL,
            'products': products,

            'order': current_order,
            'sum': total_amount,
            'user': user,
            'category': category,
            'cheapest_products': cheapest_products,
            'time_sort': time_sort,
            'products_discount': products_discount,
            'products_category': products_category,
            'count_order': count_order,
            'products_sell': products_sell,
            'header_index': header_index,
            'title_index': title_index,
            'slider_index': slider_index,
            'image_index': image_index,
            'advantage_index': advantage_index,
            'footer': footer

        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)


class ProductView(View):
    template_name = 'shop-3column.html'

    def get(self, request: HttpRequest):
        categories = request.GET.getlist('category')

        products_category = Product.objects.all()
        current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
        total_amount = sum(item.Final_Price() for item in current_order.orderdetail_set.all())
        if categories:
            products_category = Product.objects.filter(category__in=categories)

        category_name = Category.objects.all()
        orders = OrderDetail.objects.filter(order=current_order)
        count_order = 0
        for _ in orders:
            count_order += 1
        context = {
            'media_url': settings.MEDIA_URL,
            'categories': categories,
            'category_name': category_name,
            'products_category': products_category,
            'order': current_order,
            'count_order': count_order,
            'sum': total_amount
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)


class ProductDetailView(View):
    template_name = 'product-simple.html'

    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        product.visited_count += 1
        product.save()
        ratings = Rating.objects.filter(product=product_id)
        average_rating = ratings.aggregate(Avg('value'))['value__avg'] or 0

        comments = Comment.objects.filter(product=product)
        form_comment = CommentForm(initial={'user': request.user.id, 'product': product.id})
        response_comments = Response_Comment.objects.all()

        context = {
            'product': product,
            'media_url': settings.MEDIA_URL,
            'average_rating': average_rating,
            'comments': comments,
            'form_comment': form_comment,
            'response_comments': response_comments,
        }

        return render(request, self.template_name, context)

    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)

        form_comment = CommentForm(request.POST)

        if form_comment.is_valid():
            comment_instance = Comment.objects.create(product=product, user=request.user,
                                                      description=form_comment.cleaned_data['description'])

        comments = Comment.objects.filter(product=product)

        context = {
            'product': product,
            'media_url': settings.MEDIA_URL,
            'comments': comments,
            'form_comment': form_comment,

        }

        return render(request, self.template_name, context)


class Response_CommentView(View):
    template_name = 'product-simple.html'

    def get(self, request):
        return render(request, self.template_name, )

    def post(self, request: HttpRequest):
        comment_id = request.POST.get('comment_id')
        comment_value = request.POST.get('comment_value')
        get_comment = Comment.objects.get(id=comment_id)

        if request.user.is_authenticated is None:
            return JsonResponse({
                'success': False,
                'message': 'شما ورود نکردید',
                'url': 'account_shop_project/login'
            })

        Response_Comment.objects.create(comment=get_comment, user=request.user,
                                        response=comment_value)

        return JsonResponse({
            'success': True,
            'message': 'پاسخ شما ثبت و پس از تایید ادمین نمایش داده می شود',
        })


def rate_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    rate = Rating.objects.filter(product_id=product_id).first()
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rate.value = form.cleaned_data['value']
            rate.save()

            return redirect('blog:product-detail', product_id)
    else:
        form = RatingForm()

    context = {
        'form': form,
        'product': product
    }
    return render(request, 'rate_product.html', context)


def product_search(request: HttpRequest):
    query = request.GET.get('q')
    results = []

    if query:
        results = Product.objects.filter(title__icontains=query)
    context = {
        'results': results,
        'query': query,
        'media_url': settings.MEDIA_URL
    }
    return render(request, 'product_search.html', context)


class Product_api(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class Category_api(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
