from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'phone_number', 'home_address','cnic']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_cnic(self):
        cnic = self.cleaned_data['cnic']
        if User.objects.filter(cnic=cnic).exists():
            raise forms.ValidationError('CNIC must be unique.')
        return cnic

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError('Phone number must be unique.')
        return phone_number