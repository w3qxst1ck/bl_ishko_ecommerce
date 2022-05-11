from django.db.models import Q
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from cart.models import Order
from .models import WishProduct, UserInfo
from shop.models import Product


@login_required
def wish_list(request):
    wish_products = WishProduct.objects.filter(user=request.user).order_by('-adding_date')
    context = {'wish_products': None}
    if len(wish_products) > 0:
        context = {'wish_products': wish_products}
    return render(request, 'users/wishlist.html', context=context)


@login_required
def add_item_to_wish_list(request, slug):
    product = get_object_or_404(Product, slug=slug)
    wishlist_qs = WishProduct.objects.filter(user=request.user, product=product)
    if not wishlist_qs.exists():
        WishProduct.objects.create(product=product, user=request.user)
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
    return redirect('users:wishlist-page')


@login_required
def profile(request):
    if request.method == 'POST':
        user = get_object_or_404(User, id=request.user.id)
        user_info = get_object_or_404(UserInfo, user=user)
        query_post = request.POST
        for field in ['first_name', 'last_name']:
            if query_post[field] != getattr(user, field, None):
                setattr(user, field, query_post[field])
        for field in ['region', 'index', 'city', 'address', 'phone']:
            if query_post[field] != getattr(user_info, field, None):
                setattr(user_info, field, query_post[field])
        user.save()
        user_info.save()
        return redirect('users:profile-page')
    return render(request, 'users/profile.html')


@login_required
def profile_orders(request):
    orders = Order.objects.filter(user=request.user).filter(~Q(is_active=True) | ~Q(ordered=False))
    return render(request, 'users/profile_orders.html', {'orders': orders})


