from django.urls import path
from .views import ProductDetailView, Index, delivery_terms, payment_terms, order_checkout, Cart, \
    CartView

app_name = 'cafe'

urlpatterns = [
    path('', Index.as_view(), name='main_page'),
    path('cafe/cart/', CartView.as_view(), name='cart'),
    path('cafe/update-cart/', CartView.as_view(), name='update-cart'),
    # path('cafe/cart/', cart, name='cart'),
    #path('cafe/update-cart/', update_cart, name='update-cart'),
    path('cafe/product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('cafe/delivery_terms/', delivery_terms, name='delivery_terms'),
    path('cafe/payment_terms/', payment_terms, name='payment_terms'),
    path('cafe/order_checkout/', order_checkout, name='order_checkout'),
    path('cafe/<str:group>/', Index.as_view(), name='main_page'),

]
