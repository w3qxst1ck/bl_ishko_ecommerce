from django.urls import path

from .views import start_page

app_name = 'shop'

urlpatterns = [
    path('', start_page),

]
