from django.urls import path

from cart import views
from cart.views import CartAddView, CartRemoveView

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<slug:product_slug>/', CartAddView.as_view(), name='cart_add'),
    path('remove/<slug:product_slug>/', CartRemoveView.as_view(), name='cart_remove'),
]
