import re

from rest_framework import serializers
from account.models import User, CustomerAdd


class CreateUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'password1')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        password = attrs.get('password')
        password1 = attrs.pop('password1')
        errors = []
        if password != password1:
            errors.append("Passwords don't match")
        if not re.search(r'[A-Z]', password):
            errors.append('Password must contain at least one capital letter')
        if len(password) < 6:
            errors.append('Password must be at least 6 characters')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append('Password must contain at least one character of !@#$%^&*(),.?":{}|<>')
        if errors:
            raise serializers.ValidationError(errors)
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
