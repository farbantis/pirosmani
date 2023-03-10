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
    total_value = 0
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, is_completed=False)
        cart_content = order.orderitems_set.filter(quantity__gt=0)
        products = ''
    else:
        cart_content = json.loads(request.COOKIES.get('cart', '[]'))
        if cart_content:
            cart_content = {int(key): value for key, value in cart_content.items()}
            products = Product.objects.filter(id__in=cart_content.keys())
            for product in products:
                product.quantity = cart_content[product.id]['quantity']
                product.total = float(cart_content[product.id]['quantity'] * product.price)
                total_value += product.total
        order = {}

    context = {
        'cart_content': cart_content,
        'order': order,
        'pcs_ordered': len(cart_content)
        }
    if total_value:
        context.update({'total_value': total_value, 'product': products})
    return render(request, 'cafe/cart.html', context)


def update_cart(request):
    """handles all CRUD on cart - JS"""
    data = json.loads(request.body)
    productId = int(data['productId'])
    action = data['action']
    product = Product.objects.get(id=productId)
    print(f'PRODUCT {product}')

    if request.user.is_authenticated:
        print('AUTHENTICATED')
        # Get or create cart for logged in user
        order, created = Order.objects.get_or_create(customer=request.user, is_completed=False)
        print(f'order {order}')
        order_item, created = OrderItems.objects.get_or_create(order=order, product=product)
        match action:
            case 'add':
                order_item.quantity += 1
                order_item.save()
            case 'remove':
                order_item.quantity -= 1
                if order_item.quantity <= 0:
                    order_item.delete()
                else:
                    order_item.save()
            case 'removeOrderItem':
                print('removing.....')
                order_item.delete()
        pcs_ordered = OrderItems.objects.filter(order=order).count()
        information = {
            'quantity': order_item.quantity,
            'total_item': order_item.get_items_cost,
            'productId': order_item.product.id,
            'pcs_ordered': pcs_ordered
        }
        return JsonResponse(information, safe=False)
    else:
        print('ANONYMOUS USER IN ACTION')
        # handle cart for anonymous user
        cart = json.loads(request.COOKIES.get('cart', '[]'))
        cart = {int(key): value for key, value in cart.items()}

        # case action:
        match action:
            case 'add':
                if productId not in cart:
                    cart.update({productId: {
                        'product': product.name,
                    }})
                cart[productId]['quantity'] = cart[productId].get('quantity', 0) + 1
                cart[productId]['total_item'] = float(product.price * cart[productId]['quantity'])
            case 'remove':
                cart[productId]['quantity'] = cart[productId].get('quantity', 0) - 1
                if cart[productId]['quantity'] <= 0:
                    cart[productId]['quantity'] = 0
                    del cart[productId]
            case 'removeOrderItem':
                cart[productId]['quantity'] = 0
                del cart[productId]
            case _:
                raise ValueError('unexpected data')

        information = {
            'quantity': cart[productId].get('quantity', 0) if cart.get(productId, 0) else 0,
            'total_item': cart[productId].get('quantity', 0) * product.price if cart.get(productId, 0) else 0,
            'productId': productId,
            'pcs_ordered': len(cart)
        }
        response = JsonResponse(information)
        # cart = {}
        response.set_cookie('cart', json.dumps(cart))
        return response


def delivery_terms(request):
    return render(request, 'cafe/delivery_terms.html')


def payment_terms(request):
    return render(request, 'cafe/payment_terms.html')


def order_checkout(request):
    order = Order.objects.get(customer=request.user, is_completed=False)
    order.is_completed = True
    order.save()
    return redirect('/')
