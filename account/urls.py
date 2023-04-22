from django.urls import path
from account.views import RegisterUserView, UserLoginView, user_dashboard, order_history, UserLogoutView, \
    ChangeUserDetailsView

app_name = 'account'

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('user_edit/<int:pk>', ChangeUserDetailsView.as_view(), name='user_edit'),
    path('user_dashboard/', user_dashboard, name='user_dashboard'),
    path('order_history/', order_history, name='order_history'),
    # path('password_change/', UserPasswordChangeView.as_view(), name='password_change'),
]
