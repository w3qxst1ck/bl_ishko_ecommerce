from django.urls import path

from .views import add_to_cart, cart_page

app_name = 'cart'

urlpatterns = [
    path('', cart_page, name='cart-page'),
    path('<str:slug>/', add_to_cart, name='add-to-cart'),
]
