from django.contrib import admin
from .models import Order, OrderItem, BillingInfo

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(BillingInfo)