from django.contrib import admin
from .models import WishProduct, ProductComment


@admin.register(WishProduct)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product')
    list_display_links = ('id', 'user', 'product')
    list_filter = ('user', 'product')
    search_fields = ('user', 'product')


admin.site.register(ProductComment)
