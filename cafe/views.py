import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from .models import Menu, Product, Order, OrderItems


class Index(ListView):
    """shows the index page with dishes"""
    template_name = 'cafe/index.html'
    context_object_name = 'offer'

    def get_queryset(self):
        group = self.kwargs.get('group')
        if group:
            queryset = Product.objects.filter(group_id=group)
        else:
            queryset = Product.objects.all()
        return queryset


class ProductDetailView(DetailView):
    """shows detals for dish including comments calories and description"""
    model = Product
    context_object_name = 'product'
    template_name = 'cafe/product_detail.html'


def cart(request):
    """handles cart details"""
    menu = Menu.objects.all()
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, is_completed=False)
        cart_content = order.orderitems_set.filter(quantity__gt=0)
        cart_quantity = order.get_oder_quantity
    else:
        return redirect('/')

    # cart_items = order['get_cart_items']
    context = {
        'cart_content': cart_content,
        'cart_quantity': cart_quantity,
        'order': order, 'menu': menu}
    return render(request, 'cafe/cart.html', context)


def update_cart(request):
    """handles all crud on cart - js"""
    data = json.loads(request.body)
    # print(f'data is {data}')
    productId = data['productId']
    action = data['action']
    product = Product.objects.get(id=productId)
    customer = request.user
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
    # print(f'orderitem {orderItem} {orderItem.quantity}, created {created} and orderItemCost is {orderItem.get_items_cost} and grandtotal is {order.get_order_cost}')
    information = {
        'quantity': orderItem.quantity,
        'total_item': orderItem.get_items_cost,
        'grand_total': order.get_order_cost,
        'productId': orderItem.product.id
    }
    return JsonResponse(information, safe=False)


def delivery_terms(request):
    return render(request, 'cafe/delivery_terms.html')


def payment_terms(request):
    return render(request, 'cafe/payment_terms.html')


def order_checkout(request):
    order = Order.objects.get(customer=request.user, is_completed=False)
    order.is_completed = True
    order.save()
    return redirect('/')
