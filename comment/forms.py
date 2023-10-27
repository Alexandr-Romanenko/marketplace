from django import forms
from django.contrib import messages
from comment.models import Comment
from product.models import Product
from custom_user.models import CustomUser
from main_app.exceptions import ValidationError


class CommentCreationForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('content'):            
            raise forms.ValidationError('This field is required!')
        try:
            content = self.cleaned_data.get('content')
            if len(content) < 10:
                raise forms.ValidationError('This field is required!')
        except Product.DoesNotExist:
            raise ValidationError("Required fild is absence!")           
        except CustomUser.DoesNotExist:            
            raise ValidationError("Required fild is absence!")






