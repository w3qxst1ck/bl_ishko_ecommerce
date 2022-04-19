
from django.urls import path

from .views import (home_page, faq_page, product_detail, about_page,
                    shop_page, contact_page, checkout_page, category_shop_page,
                    wishlist_page)


app_name = 'shop'

urlpatterns = [
    path('', home_page, name='home-page'),
    path('faq/<int:pk>/', faq_page, name='faq-page'),
    path('checkout/', checkout_page, name='checkout-page'),
    path('contact/', contact_page, name='contact-page'),
    path('detail/<str:slug>/', product_detail, name='detail-page'),
    path('about/', about_page, name='about-page'),
    path('shop/', shop_page, name='shop-page'),
    path('shop/<str:slug>/', category_shop_page, name='cat-shop-page'),
    path('wishlist/', wishlist_page, name='wishlist-page'),
]
