from django.urls import path
from Order import views

app_name = "order"

urlpatterns = [
    path('orders/', views.add_product_to_order, name='add_orders'),
    path('remove_order/', views.remove_from_cart, name='remove_order'),
    path('add_order/', views.add_from_cart, name='add_from_cart'),
    path('request-payment/', views.request_payment, name='request_payment'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('order/api', views.Order_api.as_view(), name='order_api'),
    path('order_detail/api', views.OrderDetail_api.as_view(), name='order_api')

]
