from django.urls import path

from .views import add_to_cart, cart_page, delete_from_cart, delete_all_from_cart, checkout_order

app_name = 'cart'

urlpatterns = [
    path('', cart_page, name='cart-page'),
    path('add/<int:pk>/', add_to_cart, name='add-to-cart'),
    path('delete/all/', delete_all_from_cart, name='cart-delete-all'),
    path('delete/<int:pk>/', delete_from_cart, name='cart-delete-item'),
    path('checkout/', checkout_order, name='checkout-order')
]
