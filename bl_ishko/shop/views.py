from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Product, Category


def home_page(request):
    return render(request, 'shop/base.html')


def faq_page(request):
    return render(request, 'shop/faq.html')


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'shop/detail.html', context={'product': product})


def about_page(request):
    return render(request, 'shop/about.html')


def shop_page(request):
    products = Product.objects.all()
    return render(request, 'shop/shop.html', {'products': products})


def category_shop_page(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'shop/shop.html', {
        'products': products,
        'category': category
    })


def contact_page(request):
    return render(request, 'shop/contact.html')


def cart_page(request):

    return render(request, 'shop/cart.html')


def checkout_page(request):
    return render(request, 'shop/checkout.html')


def wishlist_page(request):
    return render(request, 'shop/wishlist.html')

