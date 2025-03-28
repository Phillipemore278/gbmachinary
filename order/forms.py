from django import forms

from .models import Order

class EditOrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['status', 'paid', 'shipping_price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control mb-3'})