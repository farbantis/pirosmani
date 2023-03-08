from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from account.forms import UserRegistrationForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.views.generic import ListView, CreateView, UpdateView
from .forms import UserRegistrationForm
from account.models import Customer


class RegisterUserView(CreateView):
    template_name = 'account/user_register.html'
    model = Customer
    form_class = UserRegistrationForm

    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            messages.add_message(request, messages.SUCCESS, f'user was created')
            return redirect('shop:login')
        return render(request, 'account/user_register.html', {'form': form})


class UserLoginView(LoginView):
    """logging user"""
    template_name = 'account/user_login.html'
    # next_page = 'cafe:main_page'

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        if self.request.user.is_staff:
            pass
            # redirect_to = '/review_merchandise/'
        else:
            return '/'


class UserLogoutView(LogoutView):
    """logout user"""
    # next_page = reverse_lazy('cafe:main_page')


#
# class UserPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
#     template_name = 'cafe/registration/../account/templates/account/change_password.html'
#     success_url = reverse_lazy('cafe:user_dashboard')
#     success_message = 'Пароль пользователя изменен'

class UserPasswordChangeView(PasswordChangeView):
    pass


class UserPasswordChangeDoneView(PasswordChangeDoneView):
    pass

def register(request):
    pass
    # if request.method == 'POST':
    #     user_form = UserRegistrationForm(request.POST)
    #     print('ready.....')
    #     if user_form.is_valid():
    #         user_data = user_form.cleaned_data
    #         print(f'user data {user_data}')
    #         user = User.objects.create_user(username=user_data['username'],
    #                                         password=user_data['password'])
    #         print(f'user is {user} {user.username}')
    #         Customer.objects.create(user_id=user.id)
    # else:
    #     user_form = UserRegistrationForm()
    #
    # context = {'user_form': user_form}
    # return render(request, 'cafe/registration/../account/templates/account/registration.html', context)