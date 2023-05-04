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
