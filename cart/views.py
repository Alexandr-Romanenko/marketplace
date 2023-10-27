from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, FormView, DeleteView

from main_app.permission_mixins import UserLoginRequiredMixin
from product.models import Product
from cart.cart import Cart
from cart.forms import CartAddProductForm


class CartAddView(UserLoginRequiredMixin, FormView):
    template_name = 'cart/detail.html'
    # queryset = Product.objects.all()
    form_class = CartAddProductForm
    success_url = '/cart'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request,
                       'slug': self.kwargs['product_slug']})
        return kwargs

    def form_valid(self, form):
        product_slug = self.kwargs.get('product_slug') or self.request.GET.get('product_slug')
        obj = Product.objects.get(slug=product_slug)
        cart = Cart(self.request)
        cd = form.cleaned_data
        cart.add(product=obj,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
        obj.quantity -= form.cleaned_data['quantity']
        obj.save()
        return super().form_valid(form=form)

    def form_invalid(self, form):
        product_slug = self.kwargs['product_slug']
        return HttpResponseRedirect(f'/product/detail/{product_slug}')



class CartRemoveView(UserLoginRequiredMixin, DeleteView):    
    slug_url_kwarg = 'slug'
    template_name = 'cart/detail.html'
    success_url = '/cart/detail/'
    queryset = Product.objects.all()

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        slug = self.kwargs.get('product_slug') or self.request.GET.get('product_slug')
        queryset = queryset.filter(slug=slug)
        obj = queryset.get()
        cart = Cart(self.request)
        cart.remove(obj)

        return obj


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True})
    return render(request, 'cart/detail.html', {'cart': cart})
