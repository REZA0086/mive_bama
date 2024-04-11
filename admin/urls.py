from django.urls import path
from . import views

app_name = "panel"

urlpatterns = [
    path('', views.PanelView.as_view(), name='panel'),
    path('products/', views.ProductView.as_view(), name='products'),
    path('product_edit/<int:product_id>/', views.EditProductView.as_view(), name='product_edit'),
    path('product_add/', views.AddProductView.as_view(), name='product_add'),
    path('product_delete/<int:product_id>/', views.delete_product, name='product_delete'),
    path('add_article/', views.AddArticleView.as_view(), name='add_article'),
    path('articles/', views.ArticlesView.as_view(), name='articles'),
    path('article_delete/<int:article_id>/', views.delete_article, name='article_delete'),
    path('edit_article/<int:article_id>/', views.ArticleDetailView.as_view(), name='edit_article'),
    path('invoice/', views.InvoiceView.as_view(), name='invoice'),
    path('invoice_delete/<int:invoice_id>/', views.invoice_delete, name='invoice_delete'),
    path('invoice_admin_detail/', views.InvoiceDetailView.as_view(), name='invoice_admin_detail'),
    path('invoice_edit/<invoice_id>/', views.EditInvoiceView.as_view(), name='invoice_edit'),
    path('invoice_add/', views.AddInvoiceView.as_view(), name='invoice_add'),
    path('add_invoice_item/', views.AddInvoiceDetailView.as_view(), name='add_invoice_item'),
    path('edit_invoice_item/<invoice_id>/', views.EditInvoiceDetailView.as_view(), name='edit_invoice_item'),
    path('invoice_item_delete/<int:invoice_id>/', views.invoice_item_delete, name='invoice_item_delete'),
    path('users_admin/', views.UsersAdmin.as_view(), name='users_admin'),
    path('delete_user/<int:user_id>', views.delete_user, name='delete_user'),
    path('add_user/', views.AddUserView.as_view(), name='add_user')


]
