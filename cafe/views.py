import json
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from .models import Product, Order, OrderItems


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
    print('DISPLAYING CART')
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, is_completed=False)
        cart_content = order.orderitems_set.filter(quantity__gt=0)
        print('content', cart_content)
        products = ''
    else:
        cart_content = json.loads(request.COOKIES.get('cart', '[]'))
        print(f'zero rem before {cart_content}')
        cart_content = {int(key): value for key, value in cart_content.items() if value['quantity'] > 0}
        print(f'zero rem after {cart_content}')
        products = Product.objects.filter(id__in=cart_content.keys())
        print(cart_content)
        for product in products:
            product.quantity = cart_content[product.id]['quantity']
            product.total = cart_content[product.id]['quantity'] * product.price
        order = {}
        print(products)

    context = {
        'cart_content': cart_content,
        'order': order,
        'product': products
        }
    return render(request, 'cafe/cart.html', context)


def update_cart(request):
    """handles all CRUD on cart - JS"""
    print('UPDATING CART')
    data = json.loads(request.body)
    productId = int(data['productId'])
    action = data['action']
    print(f'product id is {productId}, {type(productId)}')
    product = Product.objects.get(id=productId)
    print(f'action is {action}')
    print(f'product is {product}')

    if request.user.is_authenticated:
        print('USER AUTHENTICATED')
        # Get or create cart for logged in user
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, is_completed=False)
        order_item, created = OrderItems.objects.get_or_create(order=order, product=product)
        if action == 'add':
            order_item.quantity += 1
            order_item.save()
        elif action == 'remove':
            order_item.quantity -= 1
            if order_item.quantity <= 0:
                order_item.delete()
            else:
                order_item.save()
        elif action == 'removeOrderItem':
            order_item.delete()
        information = {
            'quantity': order_item.quantity,
            'total_item': order_item.get_items_cost,
            'productId': order_item.product.id
        }
        return JsonResponse(information, safe=False)
    else:
        print('USER IS ANONYMOUS')
        # Get cart from cookies for anonymous user
        cart = json.loads(request.COOKIES.get('cart', '[]'))
        cart = {int(key): value for key, value in cart.items()}
        print(f'cart is {cart}')
        # cart.setdefault(productId, )

        if action == 'add':
            if productId not in cart:
                print('productID not in cart')
                cart.update({productId: {
                    'product': product.name,
                    'quantity': 0,
                    'total_item': product.price * cart['quantity']
                }})
            cart[productId]['quantity'] = cart[productId].get('quantity', 0) + 1
        elif action == 'remove':
            cart[productId]['quantity'] = cart[productId].get('quantity', 0) - 1
            if cart[productId]['quantity'] <= 0:
                cart[productId]['quantity'] = 0
                # del cart[productId]
        elif action == 'removeOrderItem':
            cart[productId]['quantity'] = 0
            # del cart[productId]
        print(f'cart after action {cart}')
        information = {
            'quantity': cart[productId].get('quantity', 0),
            'total_item': cart[productId].get('quantity', 0) * product.price,
            'productId': productId
        }
        response = JsonResponse(information)
        response.set_cookie('cart', json.dumps(cart))
        return response




# def update_cart(request):
#     """actions for a single item - handles all crud on cart item - js"""
#     data = json.loads(request.body)
#     productId = data['productId']
#     action = data['action']
#     product = Product.objects.get(id=productId)
#     if request.user.is_authenticated:
#         order, created = Order.objects.get_or_create(customer=request.user, is_completed=False)
#         orderItem, created = OrderItems.objects.get_or_create(order=order, product=product)
#     else:
#         # Need to get one needed item Get cart from cookies for anonymous user
#         cart = json.loads(request.COOKIES.get('cart', '[]'))
#         print('THIS IS THE CART FOR ANONYMOUS')
#         print(f'cart {cart}')
#         orderItem = None
#         if cart:
#             print('in cart 1')
#             for item in cart:
#                 if item['productId'] == productId:
#                     orderItem = {
#                         'product': product,
#                         'quantity': item['quantity'],
#                         'item_total': item['quantity'] * product.price
#                     }
#                     break
#         if not orderItem:
#             print('in cart 2')
#             orderItem = {
#                 'product': product,
#                 'quantity': 0,
#                 'item_total': 0 * product.price
#             }
#
#     if action == 'add':
#         orderItem['quantity'] += 1
#         orderItem.save()
#     elif action == 'remove':
#         orderItem.quantity -= 1
#         if orderItem.quantity <= 0:
#             orderItem.delete()
#         else:
#             orderItem.save()
#     elif action == 'removeOrderItem':
#         orderItem.delete()
#
#     information = {
#         'quantity': orderItem.quantity,
#         'total_item': orderItem.get_items_cost,
#         # 'grand_total': order.get_order_cost,
#         'productId': orderItem.product.id
#     }
#     return JsonResponse(information, safe=False)


def delivery_terms(request):
    return render(request, 'cafe/delivery_terms.html')


def payment_terms(request):
    return render(request, 'cafe/payment_terms.html')


def order_checkout(request):
    order = Order.objects.get(customer=request.user, is_completed=False)
    order.is_completed = True
    order.save()
    return redirect('/')
