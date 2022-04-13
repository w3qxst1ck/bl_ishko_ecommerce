
from django.urls import path

from .views import (home_page, faq_page, product_detail, about_page,
                    shop_page, contact_page, cart_page, checkout_page,
                    login, wishlist_page, registration)


app_name = 'shop'

urlpatterns = [
    path('', home_page, name='home-page'),
    path('faq/', faq_page, name='faq-page'),
    path('cart/', cart_page, name='cart-page'),
    path('checkout/', checkout_page, name='checkout-page'),
    path('contact/', contact_page, name='contact-page'),
    path('detail/', product_detail, name='detail-page'),
    path('about/', about_page, name='about-page'),
    path('shop/', shop_page, name='shop-page'),
    path('wishlist/', wishlist_page, name='wishlist-page'),
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
]
