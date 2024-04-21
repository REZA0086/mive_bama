from django.urls import path
from . import views


app_name = "account_shop_project"

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('reset_password/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('activate_account/<email_active_code>', views.ActivateAccountView.as_view(), name='activate_account'),
    path('change_password/<str:active_code>', views.ChangePasswordView.as_view(), name='change_password'),
    path('factor/', views.Factor.as_view(), name='factor'),
    path('factor/<order_id>', views.factor_detail,name='factor_detail'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('user/api/',views.User_api.as_view(),name='user_api'),
    path('return/<order_id>/', views.Return, name='return'),
    path('logout/', views.custom_logout, name='logout')

]
