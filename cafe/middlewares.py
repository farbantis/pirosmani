from .models import Menu, Order, OrderItems


def menu_context_processor(request):
    context = dict()
    context['main_menu'] = Menu.objects.all()
    context['cart_items'] = OrderItems.objects.filter(order__customer=request.user).filter(order__is_completed=False).count()
    return context



