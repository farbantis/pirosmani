from django.urls import path
from .views import ProductDetailView, Index, delivery_terms, CartView, \
    CheckOut, payment_success, payment_fail, apply_coupon, LocationView, ReorderView, OrderPDF

app_name = 'cafe'

urlpatterns = [
    path('cafe/recreate-order/', ReorderView.as_view(), name='reorder'),
    path('cafe/location/', LocationView.as_view(), name='location'),
    path('cafe/cart/', CartView.as_view(), name='cart'),
    path('cafe/update-cart/', CartView.as_view(), name='update-cart'),
    path('cafe/product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('cafe/delivery_terms/', delivery_terms, name='delivery_terms'),
    path('cafe/checkout/', CheckOut.as_view(), name='checkout'),
    path('cafe/payment_success/', payment_success, name='payment_success'),
    path('cafe/payment_fail/', payment_fail, name='payment_fail'),
    path('cafe/order_pdf/', OrderPDF.as_view(), name='order_pdf'),
    path('cafe/apply_coupon/', apply_coupon, name='apply_coupon'),
    path('cafe/<str:group>/', Index.as_view(), name='main_page'),
    path('', Index.as_view(), name='main_page'),
]
