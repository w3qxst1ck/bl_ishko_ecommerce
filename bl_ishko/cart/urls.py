from django.urls import path

from .views import add_to_cart, cart_page, delete_from_cart

app_name = 'cart'

urlpatterns = [
    path('', cart_page, name='cart-page'),
    path('add/<int:pk>/', add_to_cart, name='add-to-cart'),
    path('delete/<int:pk>/', delete_from_cart, name='cart-delete-item'),
]
