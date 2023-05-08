from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from cafe.api.serializers import MenuListSerializer, OrderSerializer, OrderItemsSerializer
from cafe.models import Product, Order, OrderItems


class MenuListAPIView(ListAPIView):
    serializer_class = MenuListSerializer
    queryset = Product.objects.all()

    def get_queryset(self):
        qs = super(MenuListAPIView, self).get_queryset()
        id = self.kwargs.get('id')
        if id is not None:
            qs.filter(group=id)
        return qs


class OrderAPIVIewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        return super(OrderAPIVIewSet, self).get_queryset().filter(customer=self.request.user)


class OrderItemAPIVIewSet(viewsets.ModelViewSet):
    queryset = OrderItems.objects.all()
    serializer_class = OrderItemsSerializer

    def get_queryset(self):
        return super(OrderItemAPIVIewSet, self).get_queryset()\
            .filter(order__is_completed=False)\
            .filter(order__customer=self.request.user)

