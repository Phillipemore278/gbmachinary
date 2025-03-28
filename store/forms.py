from django import forms
from django.forms import inlineformset_factory

from .models import Product, Media

class AddProductForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'cols':15}),)

    class Meta:
        model = Product
        fields = ['title', 'price', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control mb-3 custom-control-input'})


class ProductMediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['image', 'is_featured']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_featured'].widget.attrs.update(
            {'class': 'form-control mb-3 form-check-input'})
        self.fields['image'].widget.attrs.update(
            {'class': 'form-control mb-3'})
            


MediaFormSet = inlineformset_factory(
    Product, Media, form=ProductMediaForm,
    extra=6, can_delete=True, can_delete_extra=False
)

EditMediaFormSet = inlineformset_factory(
    Product, Media, form=ProductMediaForm,
    extra=2, can_delete=True, can_delete_extra=False
)
