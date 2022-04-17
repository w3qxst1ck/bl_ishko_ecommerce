from django.shortcuts import render
from django.shortcuts import get_object_or_404

from allauth.account.urls import urlpatterns
from allauth.account.forms import ResetPasswordForm

from .models import Product


def home_page(request):
    return render(request, 'shop/base.html')


def faq_page(request):
    return render(request, 'shop/faq.html')


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'shop/detail.html', context={'product': product,})


def about_page(request):
    return render(request, 'shop/about.html')


def shop_page(request):
    return render(request, 'shop/shop.html')


def contact_page(request):
    return render(request, 'shop/contact.html')


def cart_page(request):

    return render(request, 'shop/cart.html')


def checkout_page(request):
    return render(request, 'shop/checkout.html')


def wishlist_page(request):
    return render(request, 'shop/wishlist.html')

