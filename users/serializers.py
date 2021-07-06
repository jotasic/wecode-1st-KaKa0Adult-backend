import re
from django.db.models import Q
from rest_framework   import serializers, status, exceptions

from .models         import User

class UserSerializer(serializers.Serializer):
    nickname     = serializers.CharField()
    email        = serializers.CharField()
    password     = serializers.CharField()
    phone_number = serializers.CharField()
    gender       = serializers.CharField()
    birth        = serializers.CharField()
 
    def create(self, validated_data):
        user = User.manager.create_user(**validated_data)
        return user

    def validate(self, data):
        RE_PASSWORD = '[a-zA-Z0-9]{5,100}'
        RE_EMAIL    = '[a-zA-Z0-9.-_+!]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]{2,}(?:.[a-zA-Z0-9]{2,3})?'

        if not re.match(RE_EMAIL, data['email']):
            error = exceptions.APIException({'message':'THE_EMAIL_IS_NOT_APPROPRIATE'})
            error.status_code = status.HTTP_400_BAD_REQUEST
            raise error

        if not re.match(RE_PASSWORD, data['password']):
            error = exceptions.APIException({'message':'THE_PASSWORD_IS_NOT_APPROPRIATE'})
            error.status_code = status.HTTP_400_BAD_REQUEST
            raise error

        if User.manager.is_duplicated_user_info(
            data['nickname'], data['email'], data['phone_number']):
                error = exceptions.APIException({'message':'DUPLICATED_CLIENT_INFORMATION'})
                error.status_code = status.HTTP_409_CONFLICT
                raise error

        return data