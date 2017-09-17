from django import forms

from orders.models import Record, Order, Label


class OrderForm(forms.ModelForm):
    zip_file = forms.FileField()

    class Meta:
        model = Order
        fields = ('name', 'verifications_needed', 'description', 'zip_file')


class LabelForm(forms.ModelForm):

    class Meta:
        model = Label
        fields = ('answer', 'record')
        widgets = {
            'record': forms.HiddenInput,
            'answer': forms.TextInput
        }