from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from users.models import WishProduct, ProductComment
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
    if request.user.is_authenticated:
        wish_list = WishProduct.objects.filter(user=request.user)
        if wish_list.exists():
            wish_list_products = [product.product for product in wish_list]
        else:
            wish_list_products = []
    else:
        wish_list_products = []
    # comments = ProductComment.objects.filter(product=product).order_by('-adding_date')
    return render(request, 'shop/detail.html', context={'product': product,
                                                        'wish_list_products': wish_list_products,
                                                        # 'comments': comments
                                                        })


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'shop/detail.html'

    def get_object(self, queryset=None):
        product = Product.objects.get(slug=self.kwargs['slug'])
        print(product.id)
        print(product.items.all())
        return product

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['wish_list_products'] = self.__get_wishlist()
        data['sorted_sizes'] = self.__sort_sizes()

    def __sort_sizes(self):
        all_sizes = ['XS', 'S', 'M', 'L', 'XL']
        sizes = [item.size.upper() for item in self.object.items.all() if item.item_count > 0]
        unique_sizes = list(set(sizes))
        return [s.upper() for s in all_sizes if s in unique_sizes]

    def __get_wishlist(self):
        if self.request.user.is_authenticated:
            wish_list = WishProduct.objects.filter(user=self.request.user)
            if wish_list.exists():
                wish_list_products = [product.product for product in wish_list]
            else:
                wish_list_products = []
        else:
            wish_list_products = []
        return wish_list_products


def shop_page(request, slug=None):
    # get products from category
    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()
    # wish product list
    if request.user.is_authenticated:
        wish_list = WishProduct.objects.filter(user=request.user)
        if wish_list.exists():
            wish_list_products = [product.product for product in wish_list]
        else:
            wish_list_products = []
    else:
        wish_list_products = []
    return render(request, 'shop/shop.html', {'products': products, 'wish_list_products': wish_list_products})


def contact_page(request):
    return render(request, 'shop/contact.html')


