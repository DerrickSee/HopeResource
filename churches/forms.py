from django import forms
from django.contrib.auth import get_user_model

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


class ChurchMembershipForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    role = forms.ChoiceField(choices=[
        ('member', 'Member'),
        ('staff', 'Staff'),
        ('owner', 'Owner'),
    ])

    class Meta:
        model = ChurchMembership
        fields = ['title']

    def save(self, commit=True):
        instance = super(ChurchMembershipForm, self).save(commit=False)
        if commit:
            data = self.cleaned_data
            user = get_user_model().objects.filter(email=data['email']).first()
            if not user:
                password = get_user_model().objects.make_random_password()
                user = get_user_model().objects.create_user(
                    first_name=data['first_name'], last_name=data['last_name'],
                    email=data['email'], password=password)
            instance.user = user
            instance.save()
        return instance
