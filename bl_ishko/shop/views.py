from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Product, Category, Faq, FaqCategory


def home_page(request):
    return render(request, 'shop/base.html')


def faq_page(request, pk):
    search_query = request.GET.get('search', '')
    faq_categories = FaqCategory.objects.all().order_by('title').exclude(title='Основные')
    faq_category = get_object_or_404(FaqCategory, id=pk)
    if request.GET.get('search'):
        faqs = Faq.objects.filter(Q(title__icontains=search_query) | Q(text__icontains=search_query))
    else:
        faqs = Faq.objects.filter(category=faq_category)
    main_category = FaqCategory.objects.filter(title='Основные')[0]
    return render(request, 'shop/faq.html', {'faqs': faqs, 'faq_categories': faq_categories,
                                             'main_category': main_category})


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

