from django.contrib import admin
from . import models


admin.site.register(models.ProductImages)
admin.site.register(models.Faq)
admin.site.register(models.FaqCategory)
admin.site.register(models.Post)


@admin.register(models.Advertising)
class AdvertisingAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_active')


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'color', 'price', 'is_active', 'discount')
    list_display_links = ('id', 'title')
    list_filter = ('category', 'color', 'price', 'discount', 'is_active')
    search_fields = ('title', 'category__title')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_active',)
    ordering = ('-created',)


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'size', 'item_count')
    list_display_links = ('id', 'product')
    list_filter = ('size', 'item_count')
    search_fields = ('product__title',)

