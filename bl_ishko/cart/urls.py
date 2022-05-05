from django.urls import path

from .views import add_to_cart, cart_page, delete_from_cart, delete_all_from_cart, order_complete_page

app_name = 'cart'

urlpatterns = [
    path('', cart_page, name='cart-page'),
    path('add/<int:pk>/', add_to_cart, name='add-to-cart'),
    path('delete/all/', delete_all_from_cart, name='cart-delete-all'),
    path('delete/<int:pk>/', delete_from_cart, name='cart-delete-item'),
    path('order_complete/', order_complete_page, name='order-complete-page'),
]
