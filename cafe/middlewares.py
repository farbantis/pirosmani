from .models import Menu, Order, OrderItems


def menu_context_processor(request):
    context = dict()
    context['main_menu'] = Menu.objects.all()

    return context



