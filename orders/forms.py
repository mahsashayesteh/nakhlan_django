from django import forms
from .models import Order


class OrderForms(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'zip_code', 'address', 'order_note']