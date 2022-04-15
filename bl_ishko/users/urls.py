from django.urls import path

from .views import wish_list, profile

app_name = 'users'

urlpatterns = [
    path('wishlist/', wish_list, name='wishlist-page'),
    path('profile/', profile, name='profile-page'),
]