from django.urls import path
from . import views

app_name = "panel"

urlpatterns = [
    path('', views.PanelView.as_view(), name='panel'),
    path('products/', views.ProductView.as_view(), name='products'),
    path('product_edit/<int:product_id>/', views.EditProductView.as_view(), name='product_edit'),
    path('product_add/', views.AddProductView.as_view(), name='product_add'),
    path('product_delete/<int:product_id>/', views.delete_product, name='product_delete'),
    path('invoice/', views.InvoiceView.as_view(), name='invoice'),
    path('invoice_delete/<int:invoice_id>/', views.invoice_delete, name='invoice_delete'),
    path('invoice_admin_detail/', views.InvoiceDetailView.as_view(), name='invoice_admin_detail'),
    path('invoice_edit/<invoice_id>/', views.EditInvoiceView.as_view(), name='invoice_edit'),
    path('invoice_add/', views.AddInvoiceView.as_view(), name='invoice_add'),
    path('add_invoice_item/', views.AddInvoiceDetailView.as_view(), name='add_invoice_item'),
    path('edit_invoice_item/<invoice_id>/', views.EditInvoiceDetailView.as_view(), name='edit_invoice_item'),
    path('invoice_item_delete/<int:invoice_id>/', views.invoice_item_delete, name='invoice_item_delete'),
    path('factor_filter/', views.FactorFilter.as_view(), name='factor_filter')




]
