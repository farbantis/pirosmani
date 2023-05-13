import json
from decimal import Decimal
import braintree
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView

from pirosmani.settings import gateway
from .mixins import ContextMixin
from .models import Product, Order, OrderItems
from .tasks import transaction_email_notification


class Index(ContextMixin, ListView):
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


class ProductDetailView(ContextMixin, DetailView):
    """shows detals for dish including comments calories and description"""
    model = Product
    context_object_name = 'product'
    template_name = 'cafe/product_detail.html'


class CartView(ContextMixin, ListView):
    template_name = 'cafe/cart.html'
    context_object_name = 'cart_content'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            customer = self.request.user
            order, created = Order.objects.get_or_create(customer=customer, is_completed=False)
            cart_content = order.orderitems_set.filter(quantity__gt=0)

        else:
            cart_content = json.loads(self.request.COOKIES.get('cart', '[]'))
            if cart_content:
                cart_content = [
                    {
                        'id': int(key),
                        'name': Product.objects.get(id=key).name,
                        'picture': Product.objects.get(id=key).picture,
                        'quantity': value,
                        'price': Product.objects.get(id=key).price
                    } for key, value in cart_content.items()]
            else:
                cart_content = []
        return cart_content

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            customer = self.request.user
            order, created = Order.objects.get_or_create(customer=customer, is_completed=False)
            total_value = order.get_order_cost
        else:
            cart_content = json.loads(self.request.COOKIES.get('cart', '[]'))
            total_value = sum([Product.objects.get(id=article).price * quantity for article, quantity in cart_content.items()])
        context_data = super(CartView, self).get_context_data()
        context_data['total_value'] = total_value
        return context_data

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        data = json.loads(request.body)
        product_id = data['productId']
        action = data['action']
        if action == 'add':
            cart_info = cart.add_item(product_id)
        elif action == 'remove':
            cart_info = cart.subtract_item(product_id)
        elif action == 'removeOrderItem':
            cart_info = cart.delete_item(product_id)
        else:
            raise ValueError('unknown command')
        response = JsonResponse(cart_info[0], safe=False)
        if request.user.is_anonymous:
            response.set_cookie('cart', json.dumps(cart_info[1]))
        return response


class Cart:
    """
    if user is authenticated we keep cart in database alternatively we keep it in cookies
    """

    def __init__(self, request):
        self.total_value = 0
        self.request = request

        if request.user.is_authenticated:
            self.customer = request.user
            self.order, self.created = Order.objects.get_or_create(customer=self.customer, is_completed=False)
            self.cart = self.order.orderitems_set.filter(quantity__gt=0)
        else:
            self.cart = json.loads(request.COOKIES.get('cart', '{}'))

    def get_cart_info_anonymous_user(self, cart, product_id=None):
        product = Product.objects.get(id=product_id) if product_id else 0
        quantity = cart.get(product_id, 0)
        total_item = quantity * product.price if product else 0
        pcs_ordered = sum([pcs for pcs in cart.values()])
        grand_total = sum([Product.objects.get(id=article).price * quantity for article, quantity in cart.items()])
        cart_info = self.make_cart_info(quantity, total_item, product_id, pcs_ordered, grand_total)
        return cart_info

    def get_cart_info_registered_user(self, item=None, order=None, product_id=None):
        quantity = item.quantity if item else 0
        total_item = float(item.get_items_cost) if item else 0
        pcs_ordered = self.order.get_oder_quantity
        grand_total = self.order.get_order_cost
        cart_info = self.make_cart_info(quantity, total_item, product_id, pcs_ordered, grand_total)
        return cart_info

    @staticmethod
    def make_cart_info(quantity, total_item, product_id, pcs_ordered, grand_total):
        cart_info = {
            'quantity': quantity,
            'total_item': total_item,
            'productId': product_id,
            'pcs_ordered': pcs_ordered,
            'grand_total': grand_total
        }
        return cart_info

    def add_item(self, product_id):
        product = Product.objects.get(id=product_id)
        if self.request.user.is_authenticated:
            item, created = OrderItems.objects.get_or_create(
                order=self.order,
                product=product,
                defaults={'quantity': 1})
            if not created:
                item.quantity += 1
                item.save()
            cart_info = self.get_cart_info_registered_user(item, self.order, product_id)
        else:
            self.cart[product_id] = self.cart.get(product_id, 0) + 1
            cart_info = self.get_cart_info_anonymous_user(self.cart, product_id)

        return cart_info, self.cart

    def subtract_item(self, product_id):
        product = Product.objects.get(id=product_id)
        if self.request.user.is_authenticated:
            item = OrderItems.objects.get(order=self.order, product=product)
            item.quantity -= 1
            item.save()
            if item.quantity <= 0:
                item.delete()
            cart_info = self.get_cart_info_registered_user(item, self.order, product_id)
        else:
            self.cart[product_id] = self.cart.get(product_id) - 1
            if self.cart[product_id] <= 0:
                del self.cart[product_id]
            cart_info = self.get_cart_info_anonymous_user(self.cart, product_id)

        return cart_info, self.cart

    def delete_item(self, product_id):
        product = Product.objects.get(id=product_id)
        if self.request.user.is_authenticated:
            item = OrderItems.objects.get(order=self.order, product=product)
            item.delete()
            cart_info = self.get_cart_info_registered_user(order=self.order)

        else:
            del self.cart[product_id]
            cart_info = self.get_cart_info_anonymous_user(cart=self.cart)
        return cart_info, self.cart


class CheckOut(View):
    def get(self, request):
        client_token = braintree.ClientToken.generate()
        order = Order.objects.get(customer=request.user, is_completed=False)
        order_items = OrderItems.objects.filter(order=order)
        context = {
            'client_token': client_token,
            'order': order,
            'order_items': order_items
        }
        return render(request, 'cafe/checkout.html', context)

    def post(self, request):
        nonce = self.request.POST.get('payment_method_nonce')
        amount = Decimal(self.request.POST.get('amount').replace(',', '.'))
        result = braintree.Transaction.sale({
            'amount': amount,
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        print('in post of payment')
        print(f'nonce, {nonce}')
        print(f'amount, {amount} {type(amount)}')
        print(f'result {result}')

        if result.is_success:
            order = Order.objects.get(customer=request.user, is_completed=False)
            order.is_completed = True
            order.transaction_id = result.transaction.id
            order.save()
            transaction_email_notification(request.user)
            return redirect('cafe:payment_success')
        else:
            # Return error response with error message
            # return JsonResponse({'success': False, 'message': result.message})
            return redirect('cafe:payment_fail')


def payment_success(request):
    return render(request, 'cafe/payment_success.html')


def payment_fail(request):
    return render(request, 'cafe/payment_fail.html')


def delivery_terms(request):
    return render(request, 'cafe/delivery_terms.html')


def payment_terms(request):
    return render(request, 'cafe/payment_terms.html')


# class GenerateTokenView(View):
#     def get(self, request, *args, **kwargs):
#         token = braintree.ClientToken.generate()
#         return JsonResponse({'token': token})
#
#
# class ProcessPaymentView(View):
#     def post(self, request, *args, **kwargs):
#         nonce = request.POST.get('payment_method_nonce')
#         amount = request.POST.get('amount')
#         result = braintree.Transaction.sale({
#             'amount': amount,
#             'payment_method_nonce': nonce,
#             'options': {
#                 'submit_for_settlement': True
#             }
#         })
#         if result.is_success:
#             return JsonResponse({'success': True})
#         else:
#             return JsonResponse({'success': False, 'message': result.message})
