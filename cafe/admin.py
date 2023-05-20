from django.contrib import admin
from .models import Product, Menu, Order, OrderItems
from import_export.admin import ExportActionMixin


class ProductAdmin(ExportActionMixin, admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


class OrderItemsInlineAdmin(admin.TabularInline):
    model = OrderItems
    raw_id_fields = ('order', )


class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'date_ordered', 'is_completed', 'transaction_id')
    list_filter = ('customer', 'date_ordered', 'is_completed')
    inlines = [OrderItemsInlineAdmin]


admin.site.register(Menu)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
