from django.shortcuts import render
from django.shortcuts import get_object_or_404

from allauth.account.urls import urlpatterns
from allauth.account.forms import ResetPasswordForm

from cart.models import Order
from .models import Product, Category


def home_page(request):
    categories = Category.objects.all().order_by('title')
    return render(request, 'shop/base.html', {'categories': categories})


def faq_page(request):
    return render(request, 'shop/faq.html')


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'shop/detail.html', context={'product': product,})


def about_page(request):
    return render(request, 'shop/about.html')


def shop_page(request):
    products = Product.objects.all()
    categories = Category.objects.all().order_by('title')
    order = get_object_or_404(Order, user=request.user)
    return render(request, 'shop/shop.html', {'products': products, 'categories': categories,
                                              'order': order})


def category_shop_page(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all().order_by('title')
    return render(request, 'shop/shop.html', {
        'products': products,
        'category': category,
        'categories': categories
    })


def contact_page(request):
    return render(request, 'shop/contact.html')


def cart_page(request):

    return render(request, 'shop/cart.html')


def checkout_page(request):
    return render(request, 'shop/checkout.html')


def wishlist_page(request):
    return render(request, 'shop/wishlist.html')

