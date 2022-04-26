from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from users.models import WishProduct
from .models import Product, Category, Faq, FaqCategory


def home_page(request):
    return render(request, 'shop/base.html')


def faq_page(request, pk=None):
    search_query = request.GET.get('search', '')
    faq_categories = FaqCategory.objects.all().order_by('title').exclude(title='Основные')
    main_category = FaqCategory.objects.filter(title='Основные')[0]
    if pk:
        faq_category = get_object_or_404(FaqCategory, id=pk)
        faqs = Faq.objects.filter(category=faq_category)
    elif search_query:
        faqs = Faq.objects.filter(Q(title__icontains=search_query) | Q(text__icontains=search_query))
    else:
        faqs = None
    return render(request, 'shop/faq.html', {'faqs': faqs, 'faq_categories': faq_categories,
                                             'main_category': main_category})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'shop/detail.html', context={'product': product})


def about_page(request):
    return render(request, 'shop/about.html')


def shop_page(request, slug=None):
    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()
        if request.user.is_authenticated:
            wish_list = WishProduct.objects.filter(user=request.user)
            if wish_list.exists():
                wish_list_products = [product.product for product in wish_list]
            else:
                wish_list_products = []
        else:
            wish_list_products = []
    return render(request, 'shop/shop.html', {'products': products, 'wish_list_products': wish_list_products})


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

