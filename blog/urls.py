from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('rate/<int:product_id>/', views.rate_product, name='rate_product'),
    path('search/', views.product_search, name='search'),
    path('products/', views.ProductView.as_view(), name='products'),
    path('products/<int:product_id>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('response-comment/', views.Response_CommentView.as_view(), name='response-comment'),
    path('product/api', views.Product_api.as_view(), name='product_api'),
    path('category/api', views.Category_api.as_view(), name='category_api'),
]
