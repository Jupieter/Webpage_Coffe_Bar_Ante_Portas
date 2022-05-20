from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home_page

app_name = 'mysite'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name="home_url"),
    path('shop/', include('shop.urls', namespace='shop')),
    # path('contact/', contact_page, name="contact_url"),
    path('accounts/', include('accounts.urls')),
    path('raw_material/', include('raw_material.urls')),
    
    # path('addresses/', include('addresses.urls')),
    # path('cart/', include('carts.urls')),
    # path('search/', include('search.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


'''' urlpatterns = [
    path('', views.main_page, name='main_page'),

    path('raw_material/', include('raw_material.urls')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('admin/', admin.site.urls),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()'''
