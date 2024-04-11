from django.shortcuts import render
from django.conf import settings
from django.conf import settings
from django.contrib.auth import login
from django.http import Http404, HttpRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views.generic import View, ListView
from rest_framework import generics
from account.serializers import *
from Order.models import *
from Order.models import Order
from account.models import *
from account.forms import *

# Create your views here.
def media_admin(request):
    return {'media_url': settings.MEDIA_URL, }

class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        login_form = LoginForm()
        context = {
            'media_url': settings.MEDIA_URL,
            'form': login_form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data['email']
            user = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error('email', 'حساب کاربری شما فعال نشده است')
                else:
                    is_password = user.check_password(login_form.cleaned_data['password'])
                    if is_password:
                        login(request, user)
                        return redirect(reverse('blog:index'))
                    else:
                        login_form.add_error('email', 'ایمیل یا کلمه عبور اشتباه است')
            else:
                login_form.add_error('email', 'کاربری با این مشخصات یافت نشد')

        context = {
            'media_url': settings.MEDIA_URL,
            'form': login_form
        }
        return render(request, self.template_name, context)


class ResetPasswordView(View):
    template_name = 'reset-password.html'

    def get(self, request, *args, **kwargs):
        reset_form = ResetPasswordForm()

        context = {
            'media_url': settings.MEDIA_URL,
            'form': reset_form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        reset_form = ResetPasswordForm(request.POST)
        if reset_form.is_valid():
            user_email = reset_form.cleaned_data['email']
            user = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                pass

        context = {
            'media_url': settings.MEDIA_URL
        }
        return render(request, self.template_name, context)


class RegisterView(View):
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        context = {
            'media_url': settings.MEDIA_URL,
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user_email = form.cleaned_data.get('email')
            user_password = form.cleaned_data.get('password')
            user = User.objects.filter(email__iexact=user_email).exists()
            if user:
                form.add_error('email', 'ایمیل تکراری می باشد')
            else:
                new_user = User(
                    email=user_email,
                    email_active_code=get_random_string(72),
                    is_active=False,
                    username=username
                )
                new_user.set_password(user_password)
                new_user.save()

                return redirect(reverse('account:login'))

        context = {
            'form': form
        }

        return render(request, self.template_name, context)


class ActivateAccountView(View):
    def get(self, request, email_active_code):
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(72)
                user.save()
                return redirect(reverse('account:login'))

        raise Http404


class ChangePasswordView(View):
    template_name = 'change-password.html'

    def get(self, request, active_code):
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if user is None:
            return redirect(reverse('account:login'))
        change_form = ChangePasswordForm()
        context = {
            'media_url': settings.MEDIA_URL,
            'form': change_form,
            'user': user
        }
        return render(request, self.template_name, context)

    def post(self, request, active_code):
        change_form = ChangePasswordForm(request.POST)
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if change_form.is_valid():
            if user is None:
                return redirect(reverse('account:login'))
            user_new_password = change_form.cleaned_data['password']
            user.set_password(user_new_password)
            user.email_active_code = get_random_string(72)
            user.is_active = True
            user.save()
            return redirect(reverse('account:login'))
        context = {
            'media_url': settings.MEDIA_URL,
            'form': change_form,
            'user': user
        }
        return render(request, self.template_name, context)


class Factor(View):
    template_name = 'invoice.html'

    def get(self, request, *args, **kwargs):
        queryset = Order.objects.filter(user_id=request.user.id,is_paid=True)
        final_price = 0  #
        if queryset.exists():
            for order in queryset:
                final_price += order.calculate_total()

        context = {
            'media_url': settings.MEDIA_URL,
            'object_list': queryset,
            'final_price': final_price
        }
        return render(request, self.template_name, context)


def factor_detail(request: HttpRequest,order_id):
    order = Order.objects.filter(id=order_id,user_id=request.user.id).first()
    if order is None:
        raise Http404('سبد خرید مورد نظر یافت نشد')
    context = {
        'media_url': settings.MEDIA_URL,
        'order':order
    }
    return render(request, 'factor_detail.html',context)


class User_api(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = UserSerializer

