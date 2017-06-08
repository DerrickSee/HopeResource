from django import forms

from .models import *
from saleor.userprofile.models import Address


address_fields = ['first_name', 'last_name',
                  'street_address_1', 'street_address_2',
                  'postal_code', 'phone']

class ChurchForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    street_address_1 = forms.CharField(required=False)
    street_address_2 = forms.CharField(required=False)
    postal_code = forms.CharField(required=False)
    phone = forms.CharField(required=False)

    class Meta:
        model = Church
        fields = ['name', 'slug'] + address_fields

    def __init__(self, *args, **kwargs):
        super(ChurchForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            for field in address_fields:
                self.fields[field].initial = getattr(self.instance.address, field)

    def save(self, commit=True):
        instance = super(ChurchForm, self).save(commit=False)
        if commit:
            data = self.cleaned_data
            address = instance.address or Address()
            for field in address_fields:
                setattr(address, field, data[field])
            address.save()
            instance.address = address
            instance.save()
        return instance
