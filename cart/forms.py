from django import forms
from product.models import Product
from main_app.exceptions import ValidationError


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        if 'slug' in kwargs:
            self.product_slug = kwargs.pop('slug')
        return super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('quantity'):
            raise forms.ValidationError('You need type the quantity!')
        quantity = cleaned_data.get('quantity')
        if quantity < 1:
            raise forms.ValidationError('You need type the positive integer!')
        try:
            product = Product.objects.get(slug=self.product_slug)
            if quantity > product.quantity:
                raise forms.ValidationError('You have ordered more than products available!')

        except Product.DoesNotExist:
            raise forms.ValidationError("Required fild is absence!")



