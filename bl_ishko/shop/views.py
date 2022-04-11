from django.shortcuts import render


def home_page(request):
    return render(request, 'shop/base1.html')


def faq_page(request):
    return render(request, 'shop/faq.html')


def product_detail(request):
    return render(request, 'shop/detail.html')
