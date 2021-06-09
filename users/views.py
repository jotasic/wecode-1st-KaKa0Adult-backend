import json, re, bcrypt, jwt

from django.views import View
from django.http import JsonResponse
from django.db.models import Q

from .models import User

class SignupView(View):
    def post(self, request):
        try:
            re_email    = '/[a-zA-Z0-9.-_+!]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]{2,}(?:.[a-zA-Z0-9]{2,3})?/'
            re_password = '/[a-zA-Z0-9]{5,100}/'

            data         = json.loads(request.body)
            nickname     = data['nickname']
            email        = data['email']
            password     = data['password']
            phone_number = data['phone_number']
            gender       = data['gender']
            birth        = data['birth']

            if not re.match(re_email, email):
                return JsonResponse({'message':'THE EMAIL IS NOT APPROPRIATE'}, status=400)
        
            if not re.match(re_password, password):
                return JsonResponse({'message': 'THE PASSWORD IS NOT APPROPRIATE'}, status=400)
        
            if User.objects.filter(
                Q(nickname     = nickname)|
                Q(email        = email)|
                Q(phone_number = phone_number)).exists():
                return JsonResponse({'message':'DUPLICATED_CLIENT_INFORMATION'}, status=409)
            
            hash_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gengalt()).decode('utf-8')

            User.objects.create(
                nickname     = nickname,
                email        = email,
                password     = hash_pw,
                phone_number = phone_number,
                gender       = gender,
                birth        = birth
            )
            return JsonResponse({'message': 'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
