from django.db.models import Q
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from users.models import WishProduct, ProductComment
from .models import Product, Category, Faq, FaqCategory
from .services import get_related_products_for_detail


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
    if request.method == 'POST':
        if request.POST.get('search-field') == ' ' or not request.POST.get('search-field'):
            products = Product.objects.all()
        else:
            product_title = request.POST.get('search-field').strip()
            if request.POST.get('category-field') != 'КАТЕГОРИИ':
                products = Product.objects.filter(title__icontains=request.POST.get('search-field'),
                                                  category__title=product_title)
            else:
                products = Product.objects.filter(title__icontains=product_title)
    else:
        products = Product.objects.all()

    # get products from category
    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(category=category)
    else:
        category = None

    # get colors for sidebar
    colors = sorted(list(set([product.color for product in products])))
    colors_tuple_list = []
    for color in colors:
        product_count = products.filter(color=color).count()
        colors_tuple_list.append((color, product_count))

    # get prices from slide
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

    # get product for color
    if request.GET.get('color'):
        color = request.GET.get('color')
        products = products.filter(color=color)
    else:
        color = None

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
                                                  'category': category, 'colors_tuple_list': colors_tuple_list,
                                                  'color': color, 'min_price': min_price, 'max_price': max_price})


def search_view(request):
    if request.method == 'POST':
        searched_product_title = request.POST.get('search-field')
        searched_product_category = request.POST.get('category-field')

        if searched_product_title == ' ' or not searched_product_title:
            if searched_product_category != 'КАТЕГОРИИ':
                products = Product.objects.filter(category__title=searched_product_category)
            else:
                searched_product_title = None
                searched_product_category = None
                products = Product.objects.all()
        else:
            searched_product_title = searched_product_title.strip()
            if searched_product_category != 'КАТЕГОРИИ':
                products = Product.objects.filter(title__icontains=searched_product_title,
                                                  category__title=searched_product_category)
            else:
                searched_product_category = None
                products = Product.objects.filter(title__icontains=searched_product_title)
    else:
        # защита от запроса через url
        searched_product_title = None
        searched_product_category = None
        products = []

    # wish product list
    if request.user.is_authenticated:
        wish_list = WishProduct.objects.filter(user=request.user)
        if wish_list.exists():
            wish_list_products = [product.product for product in wish_list]
        else:
            wish_list_products = []
    else:
        wish_list_products = []
    return render(request, 'shop/search.html', context={'products': products,
                                                        'wish_list_products': wish_list_products,
                                                        'searched_title': searched_product_title,
                                                        'searched_category': searched_product_category,
                                                        })



def contact_page(request):
    return render(request, 'shop/contact.html')

