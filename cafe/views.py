import json
from collections import defaultdict
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView
from .models import Menu, Product, Order, OrderItems, Customer
from .forms import UserRegistrationForm, UserLoginForm, UserEditForm, CustomerEditForm


class UserLoginView(LoginView):
    template_name = 'cafe/registration/user_login.html'
    next_page = 'cafe:main_page'
    authentication_form = UserLoginForm


def logout_view(request):
    logout(request)
    return redirect('cafe:main_page')


class UserPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'cafe/registration/change_password.html'
    success_url = reverse_lazy('cafe:user_dashboard')
    success_message = 'Пароль пользователя изменен'


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        customer_form = CustomerEditForm(instance=request.user.customer, data=request.POST, files=request.FILES)
        if user_form.is_valid() and customer_form.is_valid():
            user_form.save()
            customer_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('cafe:user_dashboard')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        customer_form = CustomerEditForm(instance=request.user.customer)
    return render(request, 'cafe/registration/user_edit.html', {'user_form': user_form, 'customer_form': customer_form})


@login_required()
def user_dashboard(request):
    return render(request, 'cafe/registration/user_dashboard.html')


def order_history(request):
    user_orders = Order.objects.select_related('customer__user').filter(customer__user__username__exact=request.user).order_by('-date_ordered')
    user_order_items = OrderItems.objects.select_related('order__customer__user', 'product').filter(
        order__customer__user=request.user, order__is_completed=True)
    print(user_orders)
    print(user_order_items)
    context = {'user_orders': user_orders,
               'user_order_items': user_order_items,
               }
    return render(request, 'cafe/registration/order_history.html', context)


def main_page(request, group=None):
    # menu = Menu.objects.all()
    if group:
        offer = Product.objects.filter(group_id=group)
    else:
        offer = Product.objects.all()
    context = {'offer': offer}
    return render(request, 'cafe/index.html', context)


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'cafe/product_detail.html'


def cart(request):
    menu = Menu.objects.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, is_completed=False)
        cart_content = order.orderitems_set.filter(quantity__gt=0)
        cart_quantity = order.get_oder_quantity
    else:
        print('user is not defind .... no backend further')
    # cart_items = order['get_cart_items']
    context = {'cart_content': cart_content, 'cart_quantity': cart_quantity, 'order': order, 'menu': menu}
    return render(request, 'cafe/cart.html', context)


def update_cart(request):
    data = json.loads(request.body)
    print(f'data is {data}')
    productId = data['productId']
    action = data['action']
    product = Product.objects.get(id=productId)
    customer = request.user.customer
    # print(f'customer is {customer}')
    order, created = Order.objects.get_or_create(customer=customer, is_completed=False)
    orderItem, created = OrderItems.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
        orderItem.save()
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        if orderItem.quantity <= 0:
            orderItem.delete()
        else:
            orderItem.save()
    elif action == 'removeOrderItem':
        orderItem.delete()

    # print(f'order {order}, created {created}')
    print(f'orderitem {orderItem} {orderItem.quantity}, created {created} and orderItemCost is {orderItem.get_items_cost} and grandtotal is {order.get_order_cost}')
    information = {
        'quantity': orderItem.quantity,
        'total_item': orderItem.get_items_cost,
        'grand_total': order.get_order_cost,
        'productId': orderItem.product.id
    }

    return JsonResponse(information, safe=False)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            user_data = user_form.cleaned_data
            print(f'user data {user_data}')
            user = User.objects.create_user(username=user_data['username'],
                                            email=user_data['email'],
                                            first_name=user_data['first_name'],
                                            last_name=user_data['last_name'],
                                            password=user_data['password'])
            print(f'user is {user} {user.username}')
            Customer.objects.create(user_id=user.id,
                                    phone=user_data['phone'],
                                    birth_date=user_data['birth_date'])
    else:
        user_form = UserRegistrationForm

    context = {'user_form': user_form}
    return render(request, 'cafe/registration/registration.html', context)
