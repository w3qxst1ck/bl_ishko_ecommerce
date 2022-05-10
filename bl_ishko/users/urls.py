from django.urls import path
from .views import wish_list, add_item_to_wish_list, delete_item_from_wishlist, delete_all_items_from_wishlist, profile, \
    add_comment_to_product, profile_orders

app_name = 'users'

urlpatterns = [
    path('wishlist/', wish_list, name='wishlist-page'),
    path('profile/', profile, name='profile-page'),
    path('my_orders/', profile_orders, name='profile-orders-page'),
    path('wishlist/add/<str:slug>/', add_item_to_wish_list, name='wishlist-add'),
    path('wishlist/delete/all/', delete_all_items_from_wishlist, name='wishlist-delete-all'),
    path('wishlist/delete/<str:slug>/', delete_item_from_wishlist, name='wishlist-delete'),
    path('add_comment/<str:slug>/', add_comment_to_product, name='add-comment'),
]