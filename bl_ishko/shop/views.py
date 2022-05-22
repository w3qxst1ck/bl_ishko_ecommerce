from django.db.models import Q
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from users.models import WishProduct, ProductComment
from .models import Product, Category, Faq, FaqCategory
from .services import get_related_products_for_detail, get_size_list


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

    if request.method == 'POST' and request.user.is_authenticated:
        comment = ProductComment.objects.create(product=product, user=request.user)
        comment.text = request.POST['comment_text']
        comment.save()
        return redirect('shop:detail-page', slug=slug)

    related_products = get_related_products_for_detail(product)
    if request.user.is_authenticated:
        wish_list = WishProduct.objects.filter(user=request.user)
        if wish_list.exists():
            wish_list_products = [product.product for product in wish_list]
        else:
            wish_list_products = []
    else:
        wish_list_products = []
    return render(request, 'shop/detail.html', context={'product': product,
                                                        'wish_list_products': wish_list_products,
                                                        'related_products': related_products,
                                                        })


def shop_page(request, slug=None):
    # get products from category
    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()
        category = None

    # get colors for sidebar
    color_list = sorted(list(set([product.color for product in products])))

    # get sizes for sidebar
    size_list = get_size_list(products)

    # get products by price slider
    if request.GET.get('min-price'):
        min_price = float(request.GET.get('min-price'))
        products = products.filter(price__gte=min_price)
        min_price = str(min_price).replace(',', '.')
    else:
        min_price = None

    if request.GET.get('max-price'):
        max_price = float(request.GET.get('max-price'))
        products = products.filter(price__lte=max_price)
        max_price = str(max_price).replace(',', '.')
    else:
        max_price = None

    # get products by color
    if request.GET.get('color'):
        color = request.GET.get('color')
        products = products.filter(color=color)
    else:
        color = None

    # get products by size
    if request.GET.get('size'):
        size = request.GET.get('size')
        products = products.filter(items__size=size)
    else:
        size = None

    # wish product list
    if request.user.is_authenticated:
        wish_list = WishProduct.objects.filter(user=request.user)
        if wish_list.exists():
            wish_list_products = [product.product for product in wish_list]
        else:
            wish_list_products = []
    else:
        wish_list_products = []

    return render(request, 'shop/shop.html', {'products': products, 'wish_list_products': wish_list_products,
                                                  'category': category, 'color_list': color_list,
                                                  'color': color, 'min_price': min_price, 'max_price': max_price,
                                                'size_list': size_list, 'size': size})


def contact_page(request):
    return render(request, 'shop/contact.html')

