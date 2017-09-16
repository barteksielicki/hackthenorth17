from django import forms

from orders.models import Record, Order


class OrderForm(forms.ModelForm):
    type = forms.ChoiceField(Record.RECORD_CHOICES)
    zip_file = forms.FileField()

    class Meta:
        model = Order
        fields = ('name', 'verifications_needed', 'price', 'currency', 'description', 'type', 'zip_file')