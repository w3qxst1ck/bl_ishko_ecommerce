
from django.urls import path

from .views import (home_page, faq_page, product_detail,
                    shop_page, contact_page, ProductDetailView)


app_name = 'shop'

urlpatterns = [
    path('', home_page, name='home-page'),
    path('faq/', faq_page, name='faq-search'),
    path('faq/<int:pk>/', faq_page, name='faq-page'),
    path('contact/', contact_page, name='contact-page'),
    path('detail/<str:slug>/', product_detail, name='detail-page'),
    # path('detail/<str:slug>/', ProductDetailView.as_view(), name='detail-page'),
    path('shop/', shop_page, name='shop-page'),
    path('shop/<str:slug>/', shop_page, name='cat-shop-page'),
]
