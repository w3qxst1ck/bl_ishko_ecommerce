from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls', namespace='shop')),
    path('accounts/', include('allauth.urls')),
    path('user/', include('users.urls', namespace='users')),
    path('cart/', include('cart.urls', namespace='cart')),
]

handler404 = 'shop.views.handle_not_found'

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
