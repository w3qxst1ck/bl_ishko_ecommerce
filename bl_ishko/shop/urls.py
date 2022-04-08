
from django.urls import path

from .views import home_page, faq_page, product_detail

app_name = 'shop'

urlpatterns = [
    path('', home_page, name='home-page'),
    path('faq/', faq_page, name='faq-page'),
    path('detail/', product_detail, name='detail-page'),
]
