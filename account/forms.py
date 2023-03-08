from django import forms
from django.forms import TextInput

from account.models import Customer


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    password1 = forms.CharField(max_length=100, widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ['email', 'password', 'password1']
        widgets = {
            'email': TextInput(attrs={'class': 'login_username_inner', 'placeholder': 'email'}),
            'password': TextInput(attrs={'class': 'login_username_inner', 'placeholder': 'password'}),
            'password1': TextInput(attrs={'class': 'login_username_inner', 'placeholder': 'confirm password'}),
        }

    # def clean(self):
    #     cd = super().clean()
    #     if cd['password'] != cd['password1']:
    #         raise ValidationError('passwords dont match', code='invalid')
    #
    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     if len(username) < 3:
    #         raise ValidationError('username should be at least 4 characters', code='invalid')
    #     return username