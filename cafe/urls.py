from django.urls import path
from .views import ProductDetailView, Index, delivery_terms, payment_terms, CartView, \
    CheckOut, payment_success, payment_fail, order_pdf

app_name = 'cafe'

urlpatterns = [
    path('', Index.as_view(), name='main_page'),
    path('cafe/cart/', CartView.as_view(), name='cart'),
    path('cafe/update-cart/', CartView.as_view(), name='update-cart'),
    path('cafe/product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('cafe/delivery_terms/', delivery_terms, name='delivery_terms'),
    path('cafe/payment_terms/', payment_terms, name='payment_terms'),
    path('cafe/checkout/', CheckOut.as_view(), name='checkout'),
    path('cafe/payment_success/', payment_success, name='payment_success'),
    path('cafe/payment_fail/', payment_fail, name='payment_fail'),
    path('cafe/order_pdf/<int:order_id>/', order_pdf, name='order_pdf'),
    path('cafe/<str:group>/', Index.as_view(), name='main_page'),
]

# urlpatterns += [
#     path('generate-token/', GenerateTokenView.as_view(), name='generate_token'),
#     path('process-payment/', ProcessPaymentView.as_view(), name='process_payment'),
# ]
