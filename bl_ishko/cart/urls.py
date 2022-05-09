from django.urls import path

from .views import add_to_cart, cart_page, delete_from_cart, \
    delete_all_from_cart, checkout_page, order_complete_page, \
    order_complete_page_intermediate

app_name = 'cart'

urlpatterns = [
    path('', cart_page, name='cart-page'),
    path('add/<int:pk>/', add_to_cart, name='add-to-cart'),
    path('delete/all/', delete_all_from_cart, name='cart-delete-all'),
    path('delete/<int:pk>/', delete_from_cart, name='cart-delete-item'),
    path('checkout/', checkout_page, name='checkout-page'),
    path('order_complete_intermediate/', order_complete_page_intermediate, name='order-complete-page-intermediate'),
    path('order_complete/<str:uuid>/', order_complete_page, name='order-complete-page'),
]
