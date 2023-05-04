import json
from decimal import Decimal
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

    def get_context_data(self, *, object_list=None, **kwargs):
        contex_data = super(Index, self).get_context_data()
        if self.request.user.is_authenticated:
            existing_order = Order.objects.get(customer=self.request.user)
            contex_data['order_value'] = existing_order.get_order_cost or 0
            contex_data['order_quantity'] = existing_order.get_oder_quantity or 0
        return contex_data


class ProductDetailView(DetailView):
    """shows detals for dish including comments calories and description"""
    model = Product
    context_object_name = 'product'
    template_name = 'cafe/product_detail.html'


class CartView(ListView):
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
                cart_content = {int(key): value for key, value in cart_content.items()}
                products = Product.objects.filter(id__in=cart_content.keys())
                for product in products:
                    product.quantity = cart_content[product.id]['quantity']
                    product.total = float(cart_content[product.id]['quantity'] * product.price)
        return cart_content

    def get_context_data(self, *, object_list=None, **kwargs):
        contex_data = super(CartView, self).get_context_data()
        if self.request.user.is_authenticated:
            existing_order = Order.objects.get(customer=self.request.user)
            contex_data['order_value'] = existing_order.get_order_cost or 0
            contex_data['order_quantity'] = existing_order.get_oder_quantity or 0
        return contex_data


    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        data = json.loads(request.body)
        product_id = data['productId']
        action = data['action']
        print(f'action is {action}')
        if action == 'add':
            cart_info = cart.add_item(product_id)
        elif action == 'remove':
            cart_info = cart.remove_item(product_id)
        elif action == 'removeOrderItem':
            cart_info = cart.delete_item(product_id)
        else:
            raise ValueError('unknown command')
        return JsonResponse(cart_info)


class Cart:

    def __init__(self, request):
        self.total_value = 0
        self.request = request

        if request.user.is_authenticated:
            self.customer = request.user
            self.order, self.created = Order.objects.get_or_create(customer=self.customer, is_completed=False)
            self.cart_content = self.order.orderitems_set.filter(quantity__gt=0)
        else:
            self.cart = json.loads(request.COOKIES.get('cart', '{}'))
            self.cart = {int(key): value for key, value in self.cart.items()}

    def add_item(self, product_id):
        product = Product.objects.get(id=product_id)
        if self.request.user.is_authenticated:
            item_to_add, created = OrderItems.objects.get_or_create(
                order=self.order,
                product=product,
                defaults={'quantity': 1})
            if not created:
                item_to_add.quantity += 1
                item_to_add.save()
        print(f'self.order is {self.order}')
        pcs_ordered = self.order.get_oder_quantity
        cart_info = {
            'quantity': item_to_add.quantity,
            'total_item': float(item_to_add.get_items_cost),
            'productId': item_to_add.product.id,
            'pcs_ordered': pcs_ordered,
            'grand_total': self.order.get_order_cost
        }
        print(f'response is {cart_info}')
        return cart_info

    def remove_item(self, product_id):
        print('substracting....')
        product = Product.objects.get(id=product_id)
        if self.request.user.is_authenticated:
            item_to_remove = OrderItems.objects.get(order=self.order, product=product)
            item_to_remove.quantity -= 1
            item_to_remove.save()
            if item_to_remove.quantity <= 0:
                item_to_remove.delete()
        pcs_ordered = self.order.get_oder_quantity
        #pcs_ordered = OrderItems.objects.filter(order=self.order).count()

        # self.cart[product_id]['quantity'] = self.cart[product_id].get('quantity', 0) - 1
        # if self.cart[product_id]['quantity'] <= 0:
        #     self.cart[product_id]['quantity'] = 0
        #     del self.cart[product_id]
        # else:
        #     self.cart[product_id]['total_item'] = float(Product.objects.get(id=product_id).price * self.cart[product_id]['quantity'])
        # self.save()
        cart_info = {
            'quantity': item_to_remove.quantity,
            'total_item': float(item_to_remove.get_items_cost),
            'productId': item_to_remove.product.id,
            'pcs_ordered': pcs_ordered,
            'grand_total': self.order.get_order_cost
        }
        print(f'response is {cart_info}')
        return cart_info

    def delete_item(self, product_id):
        product = Product.objects.get(id=product_id)
        if self.request.user.is_authenticated:
            item_to_delete = OrderItems.objects.get(order=self.order, product=product)
            item_to_delete.delete()
        # if product_id in self.cart:
        #     del self.cart[product_id]
        #     self.save()
        pcs_ordered = self.order.get_oder_quantity
        grand_total = self.order.get_order_cost
        cart_info = {
            'quantity': 0,
            'total_item': 0,
            'productId': 0,
            'pcs_ordered': pcs_ordered,
            'grand_total': grand_total
        }
        return cart_info


    # def save(self):
    #     response = JsonResponse()
    #     response.set_cookie('cart', json.dumps(self.cart))
    #     return response

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

    if request.user.is_authenticated:
        # Get or create cart for logged in user
        order, created = Order.objects.get_or_create(customer=request.user, is_completed=False)
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

        pcs_ordered = OrderItems.objects.filter(order=order).count()
        information = {
            'quantity': order_item.quantity,
            'total_item': order_item.get_items_cost,
            'productId': order_item.product.id,
            'pcs_ordered': pcs_ordered
        }
        return JsonResponse(information, safe=False)
    else:
        # handle cart for anonymous user
        cart = json.loads(request.COOKIES.get('cart', '{}'))
        cart = {int(key): value for key, value in cart.items()}

        if action == 'add':
            if productId not in cart:
                cart.update({productId: {
                    'product': product.name,
                }})
            cart[productId]['quantity'] = cart[productId].get('quantity', 0) + 1
            cart[productId]['total_item'] = float(product.price * cart[productId]['quantity'])
        elif action == 'remove':
            cart[productId]['quantity'] = cart[productId].get('quantity', 0) - 1
            if cart[productId]['quantity'] <= 0:
                cart[productId]['quantity'] = 0
                del cart[productId]
        elif action == 'removeOrderItem':
            cart[productId]['quantity'] = 0
            del cart[productId]
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
