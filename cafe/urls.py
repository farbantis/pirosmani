from django.urls import path
from .views import ProductDetailView, Index, update_cart, cart

app_name = 'cafe'

urlpatterns = [
    # path('order_history/', order_history, name='order_history'),
    path('cafe/update-cart/', update_cart, name='update-cart'),
    path('cafe/cart/', cart, name='cart'),
    path('cafe/product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('cafe/<str:group>/', Index.as_view(), name='main_page'),
    path('', Index.as_view(), name='main_page'),
]
