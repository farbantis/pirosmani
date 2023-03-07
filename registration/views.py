# from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError
# from django.http import JsonResponse
#
# from cafe.models import Customer
# from django.shortcuts import render
# from .forms import UserRegistrationForm, CustomerRegistrationForm
#
#
# def register(request):
#     if request.method == 'POST':
#         print('got post')
#         print(request.POST.get('first_name'))
#         # user_form = UserRegistrationForm(request.POST)
#         # print(user_form)
#         # customer_form = CustomerRegistrationForm(request.POST)
#         # print('checking..')
#         # if customer_form.is_valid() and user_form.is_valid():
#         #     user_data = user_form.cleaned_data
#         #     customer_data = customer_form.cleaned_data
#         #     print(user_data)
#         #     print(customer_data)
#         #     user = User.objects.create_user(username=user_data['username'],
#         #                                     email=user_data['email'],
#         #                                     password=user_data['password'])
#         #     print(f'user is {user}')
#         #     Customer.objects.create(user_id=user.id,
#         #                             phone=customer_data['phone'],
#         #                             birth_date=customer_data['birth_date'])
#     else:
#         raise ValidationError('smth went wrong')
#
#     return JsonResponse({"status": 'Success'})
