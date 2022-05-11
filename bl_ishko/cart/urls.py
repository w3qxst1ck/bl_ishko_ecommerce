from django.urls import path

from .views import add_to_cart, cart_page, delete_from_cart, delete_all_from_cart, checkout_page, order_complete_page, \
    order_complete_page_intermediate, cancel_order, cancel_order_confirm

app_name = 'cart'

urlpatterns = [
    path('', cart_page, name='cart-page'),
    path('add/<int:pk>/', add_to_cart, name='add-to-cart'),
    path('delete/all/', delete_all_from_cart, name='cart-delete-all'),
    path('delete/<int:pk>/', delete_from_cart, name='cart-delete-item'),
    path('checkout/', checkout_page, name='checkout-page'),
    path('order_complete_intermediate/', order_complete_page_intermediate, name='order-complete-page-intermediate'),
    path('order_complete/<str:uuid>/', order_complete_page, name='order-complete-page'),
    path('cancel_order_confirm/<str:order_id>/', cancel_order_confirm, name='cancel-order-confirm'),
    path('cancel_order/<str:order_id>/', cancel_order, name='cancel-order'),
]
