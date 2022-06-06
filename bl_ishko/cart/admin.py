from django.contrib import admin
from .models import Order, OrderItem, BillingInfo

# admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(BillingInfo)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user_email', 'user', 'created', 'ordered', 'is_active', 'paid',
                    'get_order_status', 'get_order_total_price_with_sale')
