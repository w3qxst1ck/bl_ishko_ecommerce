from django.db.models import Q, Prefetch
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.postgres.search import TrigramSimilarity
import os

from .utils import gen_slug
from users.models import WishProduct, ProductComment
from .forms import FormWithCaptcha
from .models import Product, Category, Faq, FaqCategory, Post, Item, ProductImages
from .services import get_related_products_for_detail, get_size_list
from .tasks import send_messages_from_contact_task


def home_page(request):
    if request.user.is_authenticated:
        wish_list_products = WishProduct.objects.filter(user=request.user)
    else:
        wish_list_products = []

    posts = Post.objects.filter(is_active=True)[:2]
    return render(request, 'shop/base.html', context={'wish_list_products': wish_list_products,
                                                      'posts': posts,})


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
    product = get_object_or_404(Product.objects.
                                select_related('category')
                                .prefetch_related('images')
                                # .prefetch_related(Prefetch('items', queryset=Item.objects.only('id', 'size', 'item_count'))),
                                .prefetch_related('items')
                                .prefetch_related('comments'),
                                slug=slug)

    # при публикации комментария
    if request.method == 'POST' and request.user.is_authenticated:
        comment = ProductComment.objects.create(product=product, user=request.user)
        comment.text = request.POST['comment_text']
        comment.save()
        return redirect('shop:detail-page', slug=slug)

    # формирование списка похожих товаров
    related_products = get_related_products_for_detail(product)
    if request.user.is_authenticated:
        wish_list = WishProduct.objects.filter(user=request.user).select_related('product')

        if wish_list.exists():
            wish_list_products = [product.product for product in wish_list]
        else:
            wish_list_products = []
    else:
        wish_list_products = []

    domain_add_to_cart = os.getenv('DOMAIN') + '/cart/add_ajax/'
    return render(request, 'shop/detail.html', context={'product': product,
                                                        'wish_list_products': wish_list_products,
                                                        'related_products': related_products,
                                                        'domain_add_to_cart': domain_add_to_cart,
                                                        })


def shop_page(request, slug=None):
    # get products from category
    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all().order_by('-created')
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


def search_view(request):
    if request.method == 'POST':
        searched_product_title = request.POST.get('search-field')
        searched_product_category = request.POST.get('category-field')

        # если ввели пробел или пустая строка
        if searched_product_title == ' ' or not searched_product_title:
            # выбрали категорию
            if searched_product_category != 'КАТЕГОРИИ':
                products = Product.objects.filter(category__title=searched_product_category)
            # не выбрали категорию
            else:
                searched_product_title = None
                searched_product_category = None
                products = Product.objects.all().order_by('-created')

        # ввели корректное название
        else:
            searched_product_title = searched_product_title.strip()
            searched_product_slugify = gen_slug(searched_product_title)
            # выбрали категорию
            if searched_product_category != 'КАТЕГОРИИ':

                products = Product.objects.annotate(
                    similarity=TrigramSimilarity('slug', searched_product_slugify),
                ).filter(similarity__gt=0.1).order_by('-similarity').filter(category__title=searched_product_category)
            # не выбрали категорию
            else:
                searched_product_category = None
                products = Product.objects.annotate(
                    similarity=TrigramSimilarity('slug', searched_product_slugify),
                ).filter(similarity__gt=0.1).order_by('-similarity')
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
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        topic = request.POST.get('topic', None)
        message_text = request.POST.get('message')
        if request.POST.get('g-recaptcha-response') and name and email and message_text:
            send_messages_from_contact_task.delay(name, email, topic, message_text)
            return render(request, 'shop/contact.html', {'message_name': name, 'message_email': email})
    else:
        captcha = FormWithCaptcha
        return render(request, 'shop/contact.html', {'captcha': captcha})


def handle_not_found(request, exception):
    return render(request, 'shop/404.html')
