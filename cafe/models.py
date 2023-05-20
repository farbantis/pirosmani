from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

from account.models import Customer, CustomerAdd, User
from cafe.utils import MIN_DISCOUNT_OF_COUPON, MAX_DISCOUNT_OF_COUPON


class Menu(models.Model):
    name = models.CharField(max_length=50)
    picture = models.FileField(upload_to='menu/')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='наименование')
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True, verbose_name="описание")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='цена')
    weight = models.CharField(max_length=255, default=0)
    picture = models.ImageField(upload_to='products/', default='products/no-mpphoto.jpg')
    group = models.ForeignKey(Menu, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cafe:product_detail', args=[self.slug, ])


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    is_completed = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=10)
    date_ordered = models.DateTimeField(auto_now=True)

    @property
    def get_order_cost(self):
        order_items = self.orderitems_set.all()
        order_cost = sum([item.get_items_cost for item in order_items])
        return order_cost

    @property
    def get_oder_quantity(self):
        order_items = self.orderitems_set.all()
        order_quantity = sum([item.quantity for item in order_items])
        return order_quantity

    # def get_user_order_history(self):
    #     user_orders = self.objects.filter(customer__user_id=self.customer.user_id)
    #     return user_orders

    def __str__(self):
        return str(f'{self.customer} - {self.transaction_id} - {self.is_completed}')


# class OrderManager(models.Manager):
#     def get_queryset(self):
#         return super(OrderManager, self).get_queryset().filter(Customer.user)


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    @property
    def get_items_cost(self):
        items_cost = self.quantity * self.product.price
        return items_cost

    def __str__(self):
        return str(f'{self.order} - {self.product}')


class Coupon(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    code = models.CharField(max_length=15, unique=True)
    discount = models.IntegerField(
        validators=[
            MinValueValidator(MIN_DISCOUNT_OF_COUPON),
            MaxValueValidator(MAX_DISCOUNT_OF_COUPON)
        ])
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return self.code

    @property
    def is_coupon_valid(self):
        current_date = timezone.now()
        return (self.valid_from < current_date < self.valid_until) and self.is_active and (not self.is_used)
