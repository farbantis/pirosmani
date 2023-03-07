from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.forms import TextInput, EmailInput, NumberInput, DateInput
from django.urls import reverse_lazy

from cafe.models import Customer


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'login_username_inner', 'placeholder': 'имя пользователя'})
        self.fields['password'].widget.attrs.update({'class': 'login_password_inner', 'placeholder': 'пароль'})


class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'login_password_inner'})
        self.fields['new_password1'].widget.attrs.update({'class': 'login_password_inner', 'placeholder': 'новый пароль'})
        self.fields['new_password2'].widget.attrs.update({'class': 'login_password_inner'})

        # self.fields['new_password1'].widget.attrs.update({'class': 'login_password_inner', 'placeholder': 'новый пароль'})
        # self.fields['new_password2'].widget.attrs.update({'class': 'login_password_inner', 'placeholder': 'новый пароль'})


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': TextInput(attrs={'class': 'login_username_inner', 'placeholder': 'имя'}),
            'last_name': TextInput(attrs={'class': 'login_username_inner', 'placeholder': 'фамилия'}),
            'email': EmailInput(attrs={'class': 'login_username_inner', 'placeholder': 'электронная почта'})
        }


class CustomerEditForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ('phone', 'birth_date')
        widgets = {
            'phone': TextInput(attrs={'class': 'login_username_inner', 'placeholder': 'телефон'}),
            'birth_date': DateInput(attrs={'class': 'login_username_inner', 'placeholder': 'дата рождения'})
        }


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(max_length=255, widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(max_length=255, widget=forms.PasswordInput, label='Повторите пароль')
    phone = forms.CharField(max_length=50, label='Телефон')
    birth_date = forms.DateField(label='Дата рождения')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone', 'email', 'birth_date', 'password', 'password2')

    # def password1_clean(self):
    #     if self.password != self.password2:
    #         raise ValidationError('passwords not match')
    #     else:
    #         return self.password


# class CustomerRegistrationForm(forms.ModelForm):
#     class Meta:
#         model = Customer
#         fields = ('phone', 'birth_date')


