"""
URL configuration for marketplace project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from custom_user.views import RegistrationNewUser
from django.conf import settings
from django.conf.urls.static import static
from main_app.views import MarketplaceListView, page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MarketplaceListView.as_view(), name="main_page"),
    path('user/', include('custom_user.urls', namespace='user')),
    path('product/', include('product.urls', namespace='product')),
    path('marketplace/', include('main_app.urls', namespace='marketplace')),
    path('comment/', include('comment.urls', namespace='comment')),
    path('favorites/', include('favorites.urls', namespace='favorites')),
    path('cart/', include('cart.urls', namespace='cart')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found
