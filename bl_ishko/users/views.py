from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError

from .models import WishProduct
from shop.models import Product


@login_required
def wish_list(request):
    wish_products = WishProduct.objects.filter(user=request.user)
    context = {'wish_products': None}
    if len(wish_products) > 0:
        context = {'wish_products': wish_products}
    return render(request, 'users/wishlist.html', context=context)


@login_required
def add_item_to_wish_list(request, slug):
    product = get_object_or_404(Product, slug=slug)
    try:
        WishProduct.objects.create(product=product, user=request.user)
    except IntegrityError:
        pass    # поставить message о том что товар уже в избранном
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_item_from_wishlist(request, slug):
    product = get_object_or_404(Product, slug=slug)
    try:
        WishProduct.objects.get(product=product, user=request.user).delete()
    except WishProduct.DoesNotExist:
        pass
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_all_items_from_wishlist(request):
    try:
        WishProduct.objects.filter(user=request.user).delete()
    except WishProduct.DoesNotExist:
        pass
    return redirect(request.META.get('HTTP_REFERER'))


def profile(request):
    pass