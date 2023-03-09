from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.views.generic import ListView, CreateView, UpdateView

from cafe.models import Order, OrderItems
from .forms import UserRegistrationForm, UserLoginForm, UserEditForm, CustomerAddEditForm
from .models import Customer


@login_required()
def user_dashboard(request):
    return render(request, 'account/user_dashboard.html')


@login_required()
def order_history(request):
    # .select_related('customer__user')
    user_orders = Order.objects\
        .filter(customer=request.user)\
        .order_by('-date_ordered')
    # .select_related('order__customer__user', 'product')
    user_order_items = OrderItems.objects\
        .filter(order__customer=request.user)
    # , order__is_completed = True
    print(user_orders)
    print(user_order_items)
    context = {'user_orders': user_orders,
               'user_order_items': user_order_items,
               }
    return render(request, 'account/order_history.html', context)


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
            return redirect('account:login')
        else:
            form = UserRegistrationForm()
        return render(request, 'account/user_register.html', {'form': form})


class UserLoginView(LoginView):
    """logging user"""
    template_name = 'account/user_login.html'
    form_class = UserLoginForm
    next_page = 'cafe:main_page'

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        if self.request.user.is_staff:
            pass
            # redirect_to = '/review_merchandise/'
        else:
            return '/'


class UserLogoutView(LogoutView):
    """logout user"""
    next_page = reverse_lazy('cafe:main_page')


class UserPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'account/change_password.html'
    success_url = reverse_lazy('cafe:user_dashboard')
    success_message = 'Пароль пользователя изменен'


class UserPasswordChangeDoneView(PasswordChangeDoneView):
    pass


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST)
        customer_form = CustomerAddEditForm(request.POST)
        if user_form.is_valid() and customer_form.is_valid():
            user_form.save()
            customer_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('account:user_dashboard')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm()
        customer_form = CustomerAddEditForm()
    return render(request, 'account/user_edit.html', {'user_form': user_form, 'customer_form': customer_form})
