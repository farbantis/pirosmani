from django.contrib import admin
from .models import User, Customer, CustomerAdd, Admin


admin.site.register(User)
admin.site.register(Customer)
admin.site.register(CustomerAdd)
admin.site.register(Admin)
