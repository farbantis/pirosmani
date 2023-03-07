# from django import forms
# from django.contrib.auth.models import User
# from django.contrib.auth.password_validation import validate_password
# from django.core.exceptions import ValidationError
# from cafe.models import Customer
#
#
# class CustomerRegistrationForm(forms.ModelForm):
#     class Meta:
#         model = Customer
#         fields = ('phone', 'birth_date')
#
#
# class UserRegistrationForm(forms.ModelForm):
#     password = forms.CharField(max_length=255, widget=forms.PasswordInput)
#     password2 = forms.CharField(max_length=255, widget=forms.PasswordInput)
#
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'username', 'email', 'password', 'password2')
#
#     # def password1_clean(self):
#     #     if self.password != self.password2:
#     #         raise ValidationError('passwords not match')
#     #     else:
#     #         return self.password
#
#
#
#
