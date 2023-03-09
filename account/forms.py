from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django.forms import TextInput, PasswordInput, EmailInput, DateInput
from account.models import User, CustomerAdd


class UserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'login_username_inner', 'placeholder': 'email'})
        self.fields['password'].widget.attrs.update({'class': 'login_password_inner', 'placeholder': 'password'})


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        max_length=100,
        widget=PasswordInput(attrs={'class': 'login_username_inner', 'placeholder': 'confirm password'}))

    class Meta:
        model = User
        fields = ['email', 'password', 'password1']
        widgets = {
            'email': EmailInput(attrs={'class': 'login_username_inner', 'placeholder': 'email'}),
            'password': PasswordInput(attrs={'class': 'login_username_inner', 'placeholder': 'password'}),
        }

    def clean(self):
        cd = super().clean()
        if cd['password'] != cd['password1']:
            raise ValidationError('passwords dont match', code='invalid')


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': TextInput(attrs={'class': 'login_username_inner', 'placeholder': 'имя'}),
            'last_name': TextInput(attrs={'class': 'login_username_inner', 'placeholder': 'фамилия'}),
            'email': EmailInput(attrs={'class': 'login_username_inner', 'placeholder': 'электронная почта'})
        }


class CustomerAddEditForm(forms.ModelForm):

    class Meta:
        model = CustomerAdd
        fields = ('birth_date', )
        widgets = {
            'birth_date': DateInput(attrs={'class': 'login_username_inner', 'placeholder': 'дата рождения'})
        }


class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'login_password_inner'})
        self.fields['new_password1'].widget.attrs.update({'class': 'login_password_inner', 'placeholder': 'новый пароль'})
        self.fields['new_password2'].widget.attrs.update({'class': 'login_password_inner'})

        # self.fields['new_password1'].widget.attrs.update({'class': 'login_password_inner', 'placeholder': 'новый пароль'})
        # self.fields['new_password2'].widget.attrs.update({'class': 'login_password_inner', 'placeholder': 'новый пароль'})



