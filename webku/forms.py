from django import forms
from django.contrib.auth.models import User
from .models import Profile
from .models import Address

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'gender', 'birth_date']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['full_name', 'phone', 'province', 'city', 'postal_code', 'housing_address']

    def clean(self):
        cleaned_data = super().clean()
        user = self.instance.user if self.instance else None
        if user and Address.objects.filter(user=user).exists() and not self.instance.pk:
            raise forms.ValidationError('You already have an address saved.')
        return cleaned_data
    
    class AddressForm(forms.ModelForm):
        class Meta:
            model = Address
            fields = ['full_name', 'phone', 'province', 'city', 'postal_code', 'housing_address']