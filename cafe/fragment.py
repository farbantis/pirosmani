from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
@staff_member_required
def admin_order_pdf(request, order_id):
order = get_object_or_404(Order, id=order_id)
html = render_to_string('orders/order/pdf.html',
{'order': order})
response = HttpResponse(content_type='application/pdf')
response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
weasyprint.HTML(string=html).write_pdf(response,
stylesheets=[weasyprint.CSS(
settings.STATIC_ROOT + 'css/pdf.css')])
return response





REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)
r.set('foo', 'bar'); r.get('foo');
total_views = r.incr(f'image:{image.id}:views')

# match action:
#     case 'add':
#         order_item.quantity += 1
#         order_item.save()
#     case 'remove':
#         order_item.quantity -= 1
#         if order_item.quantity <= 0:
#             order_item.delete()
#         else:
#             order_item.save()
#     case 'removeOrderItem':
#         order_item.delete()

# match action:
#     case 'add':
#         if productId not in cart:
#             cart.update({productId: {
#                 'product': product.name,
#             }})
#         cart[productId]['quantity'] = cart[productId].get('quantity', 0) + 1
#         cart[productId]['total_item'] = float(product.price * cart[productId]['quantity'])
#     case 'remove':
#         cart[productId]['quantity'] = cart[productId].get('quantity', 0) - 1
#         if cart[productId]['quantity'] <= 0:
#             cart[productId]['quantity'] = 0
#             del cart[productId]
#     case 'removeOrderItem':
#         cart[productId]['quantity'] = 0
#         del cart[productId]
#     case _:
#         raise ValueError('unexpected data')

# def cart(request):
#     """handles cart details"""
#     total_value = 0
#     if request.user.is_authenticated:
#         customer = request.user
#         order, created = Order.objects.get_or_create(customer=customer, is_completed=False)
#         cart_content = order.orderitems_set.filter(quantity__gt=0)
#         products = ''
#     else:
#         cart_content = json.loads(request.COOKIES.get('cart', '[]'))
#         if cart_content:
#             cart_content = {int(key): value for key, value in cart_content.items()}
#             products = Product.objects.filter(id__in=cart_content.keys())
#             for product in products:
#                 product.quantity = cart_content[product.id]['quantity']
#                 product.total = float(cart_content[product.id]['quantity'] * product.price)
#                 total_value += product.total
#         order = {}
#
#     context = {
#         'cart_content': cart_content,
#         'order': order,
#         'pcs_ordered': len(cart_content)
#     }
#     if total_value:
#         context.update({'total_value': total_value, 'product': products})
#     return render(request, 'cafe/cart.html', context)
#
#
# def update_cart(request):
#     """handles all CRUD on cart - JS"""
#     data = json.loads(request.body)
#     productId = int(data['productId'])
#     action = data['action']
#     product = Product.objects.get(id=productId)
#
#     if request.user.is_authenticated:
#         # Get or create cart for logged in user
#         order, created = Order.objects.get_or_create(customer=request.user, is_completed=False)
#         order_item, created = OrderItems.objects.get_or_create(order=order, product=product)
#
#         if action == 'add':
#             order_item.quantity += 1
#             order_item.save()
#         elif action == 'remove':
#             order_item.quantity -= 1
#             if order_item.quantity <= 0:
#                 order_item.delete()
#             else:
#                 order_item.save()
#         elif action == 'removeOrderItem':
#             order_item.delete()
#
#         pcs_ordered = OrderItems.objects.filter(order=order).count()
#         information = {
#             'quantity': order_item.quantity,
#             'total_item': order_item.get_items_cost,
#             'productId': order_item.product.id,
#             'pcs_ordered': pcs_ordered
#         }
#         return JsonResponse(information, safe=False)
#     else:
#         # handle cart for anonymous user
#         cart = json.loads(request.COOKIES.get('cart', '{}'))
#         cart = {int(key): value for key, value in cart.items()}
#
#         if action == 'add':
#             if productId not in cart:
#                 cart.update({productId: {
#                     'product': product.name,
#                 }})
#             cart[productId]['quantity'] = cart[productId].get('quantity', 0) + 1
#             cart[productId]['total_item'] = float(product.price * cart[productId]['quantity'])
#         elif action == 'remove':
#             cart[productId]['quantity'] = cart[productId].get('quantity', 0) - 1
#             if cart[productId]['quantity'] <= 0:
#                 cart[productId]['quantity'] = 0
#                 del cart[productId]
#         elif action == 'removeOrderItem':
#             cart[productId]['quantity'] = 0
#             del cart[productId]
#         information = {
#             'quantity': cart[productId].get('quantity', 0) if cart.get(productId, 0) else 0,
#             'total_item': cart[productId].get('quantity', 0) * product.price if cart.get(productId, 0) else 0,
#             'productId': productId,
#             'pcs_ordered': len(cart)
#         }
#         response = JsonResponse(information)
#         # cart = {}
#         response.set_cookie('cart', json.dumps(cart))
#         return response
