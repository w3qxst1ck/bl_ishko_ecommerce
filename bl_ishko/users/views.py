from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required


@login_required
def wish_list(request):
    # if not request.user.is_authenticated:
    #     return reverse('account_login')
    return render(request, 'users/wishlist.html')


def profile(request):
    pass