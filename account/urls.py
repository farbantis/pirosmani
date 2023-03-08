from django.urls import path
from account.views import RegisterUserView, UserLoginView

app_name = 'account'

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    # path('logout/', logout_view, name='logout'),
    # path('password_change/', UserPasswordChangeView.as_view(), name='password_change'),
    # path('user_edit/', edit, name='user_edit'),
    # path('edit/', register, name='edit'),
    # path('user_dashboard/', user_dashboard, name='user_dashboard'),
]