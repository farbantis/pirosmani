from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from account.api.serializers import CreateUserSerializer
from account.models import User
from rest_framework.authtoken.models import Token


class CreateUserAPIView(CreateAPIView):
    """creates an instance of a cafe customer"""
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()
    http_method_names = ['post']


class LogoutAPIView(APIView):
    """logs the user out"""
    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "You are logged out."}, status=status.HTTP_200_OK)
