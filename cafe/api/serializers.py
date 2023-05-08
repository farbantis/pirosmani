from rest_framework import serializers
from cafe.models import Product, OrderItems, Order


class MenuListSerializer(serializers.ModelSerializer):
    group = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'weight', 'picture', 'group')

    def get_group(self, object):
        return object.group.name


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ('id', 'product', 'quantity', 'order')


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemsSerializer(many=True, source='orderitems_set')

    class Meta:
        model = Order
        fields = ('id', 'customer', 'is_completed', 'order_items')
        # read_only_fields = ('id', 'customer', 'is_completed')
