from django.contrib.auth.models import AbstractUser
from django.db import models
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from .tasks import change_status_notification


class User(AbstractUser):
    class Types(models.TextChoices):
        CUSTOMER = 'C', _('Customer')
        ADMIN = 'A', _('Admin')
    type = models.CharField(_('user type'), max_length=50, choices=Types.choices, default=Types.CUSTOMER)
    email = models.EmailField(_("email address"), unique=True)
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.type == self.Types.CUSTOMER:
            if not hasattr(self, 'customeradd'):
                CustomerAdd.objects.create(user_id=self.id)


class AdminManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.ADMIN)


class Admin(User):
    objects = AdminManager()

    class Meta:
        proxy = True
        verbose_name = 'Admin'
        verbose_name_plural = "Admins"


class CustomerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.CUSTOMER)


class Customer(User):
    objects = CustomerManager()

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        proxy = True


class CustomerAdd(models.Model):

    class CustomerStatusLimits:
        """sets the amount to update the status level e.g. if amount of purchase more 1000, status is Silver"""
        BRONZE = 1_000
        SILVER = 10_000
        GOLD = 100_000
        PLATINUM = 1_000_000  # we believe it's impossible for user to reach this amount
        customer_status_limits = ('BRONZE', BRONZE), ('SILVER', SILVER), ('GOLD', GOLD), ('PLATINUM', PLATINUM)

    class CustomerStatus(models.TextChoices):
        BRONZE = 'BRONZE', 'BRONZE'
        SILVER = 'SILVER', 'SILVER'
        GOLD = 'GOLD', 'GOLD'
        PLATINUM = 'PLATINUM', 'PLATINUM'

    user = models.OneToOneField(Customer, on_delete=models.CASCADE)
    birth_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=CustomerStatus.choices, default=CustomerStatus.BRONZE)
    bonus = models.IntegerField(default=0)
    amount_of_purchase = models.IntegerField(default=0)

    def __str__(self):
        return self.user.email

    @property
    def get_customer_status(self):
        """set the cinemagoer status based on the amount of purchases"""
        # !! а если бы мы хотели подсчитываеть количество изменений статуса.... => записывать кол-во в бд?..
        lst_of_status_names = [x[0] for x in CustomerAdd.CustomerStatusLimits.customer_status_limits]
        previous_status = self.status
        # getting current status
        for st in CustomerAdd.CustomerStatusLimits.customer_status_limits:
            if self.amount_of_purchase < st[-1]:
                self.status = st[0]
        #  if status has changed, we have to inform the user by email ?? and in cabinet ??!
        if previous_status != self.status:
            if lst_of_status_names.index(previous_status) < lst_of_status_names.index(self.status):
                action_status = 'going_up'
            else:
                action_status = 'going_down'
            change_status_notification(self.user, self.status, action_status)
        return self.status
