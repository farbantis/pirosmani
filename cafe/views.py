import json
import math
import braintree
import requests
import weasyprint
from decimal import Decimal
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import DetailView, ListView
from django.conf import settings
from .mixins import ContextMixin, CartActionsMixin
from .models import Product, Order, OrderItems, Coupon
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


class CartView(CartActionsMixin, ContextMixin, ListView):
    template_name = 'cafe/cart.html'
    context_object_name = 'cart_content'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            customer = self.request.user
            order, created = Order.objects.get_or_create(customer=customer, is_completed=False)
            cart_content = order.orderitems_set.filter(quantity__gt=0)

        else:
            cart_content = self.get_cookie_cart_content()
            if cart_content:
                cart_content = [
                    {
                        'id': int(key),
                        'name': Product.objects.get(id=key).name,
                        'picture': Product.objects.get(id=key).picture,
                        'quantity': value,
                        'price': Product.objects.get(id=key).price,
                        'item_value': Product.objects.get(id=key).price * value
                    } for key, value in cart_content.items()]
            else:
                cart_content = {}
        return cart_content

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            customer = self.request.user
            order, created = Order.objects.get_or_create(customer=customer, is_completed=False)
            total_value = order.get_order_cost
        else:
            cart_content = self.get_cookie_cart_content()
            total_value = sum(
                [Product.objects.get(id=article).price * quantity for article, quantity in cart_content.items()]
            )
        context_data = super(CartView, self).get_context_data()
        context_data['total_value'] = total_value
        return context_data

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        product_id = data['productId']
        cart = Cart(product_id, request)
        action = data['action']
        if action == 'add':
            cart_info = cart.add_item()
        elif action == 'remove':
            cart_info = cart.subtract_item()
        elif action == 'removeOrderItem':
            cart_info = cart.delete_item()
        else:
            raise ValueError('unknown command')
        response = JsonResponse(cart_info[0], safe=False)
        if request.user.is_anonymous:
            response.set_cookie('cart', json.dumps(cart_info[1]))
        return response


class Cart(CartActionsMixin):
    """
    if user is authenticated we keep cart in database alternatively we keep it in cookies
    """

    def __init__(self, product_id, request):
        self.request = request
        self.product_id = product_id
        self.product = get_object_or_404(Product, id=self.product_id)

        if request.user.is_authenticated:
            self.order, self.created = Order.objects.get_or_create(
                customer=self.request.user,
                is_completed=False
            )
            self.cart = self.order.orderitems_set.filter(quantity__gt=0)

        else:
            self.cart = self.get_cookie_cart_content()

    def get_cart_info_anonymous_user(self, cart, product_id=None):
        quantity = cart.get(product_id, 0)
        if product_id:
            product = Product.objects.get(id=product_id)
            total_item = quantity * product.price
        else:
            total_item = 0
        pcs_ordered = sum([pcs for pcs in cart.values()])
        grand_total = sum(
            [Product.objects.get(id=article).price * quantity for article, quantity in cart.items()]
        )
        cart_info = self.make_cart_info(quantity, total_item, product_id, pcs_ordered, grand_total)
        return cart_info

    def get_cart_info_registered_user(self, item=None, order=None, product_id=None):
        quantity = item.quantity if item else 0
        total_item = item.get_items_cost if item else 0
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

    def add_item(self):
        if self.request.user.is_authenticated:
            item, created = OrderItems.objects.get_or_create(
                order=self.order,
                product=self.product,
                defaults={'quantity': 1})
            if not created:
                item.quantity += 1
                item.save()
            cart_info = self.get_cart_info_registered_user(item, self.order, self.product_id)
        else:
            self.cart[self.product_id] = self.cart.get(self.product_id, 0) + 1
            cart_info = self.get_cart_info_anonymous_user(self.cart, self.product_id)
        return cart_info, self.cart

    def subtract_item(self):
        if self.request.user.is_authenticated:
            item = OrderItems.objects.get(order=self.order, product=self.product)
            item.quantity -= 1
            item.save()
            if item.quantity <= 0:
                item.delete()
            cart_info = self.get_cart_info_registered_user(item, self.order, self.product_id)
        else:
            self.cart[self.product_id] = self.cart.get(self.product_id) - 1
            if self.cart[self.product_id] <= 0:
                del self.cart[self.product_id]
            cart_info = self.get_cart_info_anonymous_user(self.cart, self.product_id)
        return cart_info, self.cart

    def delete_item(self):
        if self.request.user.is_authenticated:
            item = OrderItems.objects.get(order=self.order, product=self.product)
            item.delete()
            cart_info = self.get_cart_info_registered_user(order=self.order)
        else:
            del self.cart[self.product_id]
            cart_info = self.get_cart_info_anonymous_user(cart=self.cart)
        return cart_info, self.cart


class CheckOut(View):
    """checkout and payment"""

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

        if result.is_success:
            order = Order.objects.get(customer=request.user, is_completed=False)
            order.is_completed = True
            order.transaction_id = result.transaction.id
            order.save()
            #  transaction_email_notification(request.user)
            return redirect('cafe:payment_success')
        else:
            # return JsonResponse({'success': False, 'message': result.message})
            return redirect('cafe:payment_fail')


def apply_coupon(request):
    data = json.loads(request.body)
    coupon_code = data['couponCode']
    coupon = Coupon.objects.filter(code=coupon_code)[0]
    if coupon:
        if coupon.is_coupon_valid:
            coupon.owner = request.user
            coupon.save()
            discount = coupon.discount
        else:
            discount = -1
    else:
        discount = 0
    return JsonResponse({"discount": discount}, safe=False)


def payment_success(request, pdf_data):
    return render(request, 'cafe/payment_success.html', context={'pdf_data': pdf_data})


def payment_fail(request):
    return render(request, 'cafe/payment_fail.html')


class ReorderView(View):

    def get(self, request):
        new_order, created = Order.objects.get_or_create(customer=request.user, is_completed=False)
        order_id = request.GET.get('order_id')
        order_items = OrderItems.objects.filter(order_id=order_id)
        for item in order_items:
            OrderItems.objects.create(order=new_order, product=item.product, quantity=item.quantity)
        return redirect('cafe:cart')


def delivery_terms(request):
    return render(request, 'cafe/delivery_terms.html')


class LocationView(View):
    """calculates user location based ip address and finds the nearest shop to the user"""

    SHOPS = [
        (55.95073763174729, -3.1883533021694155, 'Edinburgh, unknown street 246'),
        (50.858996045327125, 4.365800266413261, 'Brussel, unknown street 246'),
        (52.43156626600185, -1.9309518016162073, 'Birminham, unknown street 246'),
        (52.21650624286724, 21.03417408205453, 'Warssaw, unknown street 246')
    ]

    @staticmethod
    def deg2rad(deg):
        return deg * (math.pi / 180)

    def get_distance(self, lat_1, lon_1, lat_2, lon_2):
        R = 6371
        d_lat = self.deg2rad(lat_2 - lat_1)
        d_lon = self.deg2rad(lon_2 - lon_1)
        a = math.sin(d_lat / 2) * math.sin(d_lat / 2) + math.cos(self.deg2rad(lat_1)) * math.cos(self.deg2rad(lat_2)) * \
            math.sin(d_lon / 2) * math.sin(d_lon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = R * c  # Distance in km
        return d

    def get_visitor_ip_address(self):
        req_headers = self.request.META
        x_forwarded_for_value = req_headers.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for_value:
            ip_addr = x_forwarded_for_value.split(',')[-1].strip()
        else:
            ip_addr = req_headers.get('REMOTE_ADDR')
        return ip_addr

    @staticmethod
    def get_lat_lon(visitor_ip_address):
        user_location_data = requests.get(f'http://ip-api.com/json/{visitor_ip_address}')  # 191.96.53.71
        user_location_data = user_location_data.json()
        return user_location_data

    def get(self, request):
        visitor_ip_address = self.get_visitor_ip_address()
        user_location_data = self.get_lat_lon(visitor_ip_address)
        lat, lon = user_location_data.get('lat', 0), user_location_data.get('lon', 0)
        if lat and lon:
            distances = [self.get_distance(lat, lon, x[0], x[1]) for x in self.SHOPS]
            closest_shop_distance = min(distances)
            closest_shop_index = distances.index(closest_shop_distance)
            closest_shop = self.SHOPS[closest_shop_index]
        else:
            closest_shop = 'no data'
        context = {
            'visitor_ip_address': visitor_ip_address,
            'user_location_data': user_location_data,
            'closest_shop': closest_shop
        }
        return render(request, 'cafe/location.html', context)


class OrderPDF(View):

    def get(self, request):
        order_id = request.GET.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        html = render_to_string('cafe/pdf_receipt.html', {'order': order})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
        weasyprint.HTML(string=html).write_pdf(
            response,
            stylesheets=[weasyprint.CSS(str(settings.STATIC_ROOT) + '/cafe/css/pdf.css')])
        return response
