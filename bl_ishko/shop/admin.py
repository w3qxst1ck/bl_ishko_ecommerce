from django.contrib import admin
from . import models


admin.site.register(models.ProductImages)


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'is_active', 'discount')
    list_display_links = ('id', 'title')
    list_filter = ('category', 'price', 'discount', 'is_active')
    search_fields = ('title', 'category__title')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_active',)


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'color', 'size', 'item_count')
    list_display_links = ('id', 'product')
    list_filter = ('color', 'size', 'item_count')
    search_fields = ('product__title',)

