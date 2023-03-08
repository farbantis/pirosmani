from django.contrib.auth.views import PasswordChangeView
from django.urls import path
from .views import *
app_name = 'cafe'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('password_change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('user_edit/', edit, name='user_edit'),
    path('user_dashboard/', user_dashboard, name='user_dashboard'),
    path('order_history/', order_history, name='order_history'),

    # path('edit/', register, name='edit'),
    # path('registration/', register, name='register'),

    path('cafe/update-cart/', update_cart, name='update-cart'),
    path('cafe/cart/', cart, name='cart'),
    path('cafe/<str:group>/', main_page, name='main_page'),
    path('', main_page, name='main_page'),
    # path('<str:group>', main_page, name='main_page'),
    path('cafe/product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
]
