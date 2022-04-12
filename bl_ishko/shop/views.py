from django.shortcuts import render


def home_page(request):
    return render(request, 'shop/base.html')


def faq_page(request):
    return render(request, 'shop/faq.html')


def product_detail(request):
    return render(request, 'shop/detail.html')


def about_page(request):
    return render(request, 'shop/about.html')

def shop_page(request):
    return render(request, 'shop/shop.html')
