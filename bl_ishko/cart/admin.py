from django.contrib import admin


from .models import Order, OrderItem, BillingInfo
from .tasks import send_message_to_client_changed_paid_status


admin.site.register(OrderItem)
admin.site.register(BillingInfo)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', '_get_user_email', 'user', 'created', 'ordered', 'is_active', 'paid',
                    '_get_order_status', 'get_order_total_price_with_sale')

    def save_model(self, request, obj, form, change):
        if change:
            if form.initial['paid'] != form.cleaned_data['paid'] and form.cleaned_data['paid']:
                send_message_to_client_changed_paid_status.delay(obj.id)
        obj.save()



