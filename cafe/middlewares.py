from .models import Menu, Order, OrderItems


def menu_context_processor(request):
    context = dict()
    context['main_menu'] = Menu.objects.all()
    if request.user.is_authenticated:
        existing_order = Order.objects.filter(customer=request.user, is_completed=False)[0]
        context['order_value'] = existing_order.get_order_cost or 0
        context['order_quantity'] = existing_order.get_oder_quantity or 0
    return context



