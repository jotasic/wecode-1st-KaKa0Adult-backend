import json, re, bcrypt, jwt

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from products.models     import Product
from .models             import User, Like
from users.utils         import login_decorator
from kaka0Adult.settings import SECRET_KEY, ALGORITHM

class SignupView(View):
    def post(self, request):
        try:
            re_email    = '[a-zA-Z0-9.-_+!]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]{2,}(?:.[a-zA-Z0-9]{2,3})?'
            re_password = '[a-zA-Z0-9]{5,100}'

            data         = json.loads(request.body)
            nickname     = data['nickname']
            email        = data['email']
            password     = data['password']
            phone_number = data['phone_number']
            gender       = data['gender']
            birth        = data['birth']

            if not re.match(re_email, email):
                return JsonResponse({'message':'THE_EMAIL_IS_NOT_APPROPRIATE'}, status=400)
        
            if not re.match(re_password, password):
                return JsonResponse({'message':'THE_PASSWORD_IS_NOT_APPROPRIATE'}, status=400)
            
            if User.objects.filter(
                Q(nickname     = nickname)|
                Q(email        = email)|
                Q(phone_number = phone_number)).exists():
                return JsonResponse({'message':'DUPLICATED_CLIENT_INFORMATION'}, status=409)
            
            hash_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                nickname     = nickname,
                email        = email,
                password     = hash_pw,
                phone_number = phone_number,
                gender       = gender,
                birth        = birth
            )
            return JsonResponse({'message':'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

class LoginView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']

            if not User.objects.filter(email = email).exists():
                return JsonResponse({'message':'INVALID_USER'}, status = 401)
            
            user = User.objects.get(email = email)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message':'INVALID_USER'},status=401)

            access_token = jwt.encode({'id':user.id}, SECRET_KEY,ALGORITHM)
            
            return JsonResponse({'message':'LOGIN_SUCCESS','token':access_token,'user_name':user.nickname}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
    
class LikeView(View):
    @login_decorator
    def post(self, request):
        try:
            data       = json.loads(request.body)
            product_id = data['product_id']
            user       = request.user
        
            if not Product.objects.filter(id = product_id ).exists():
                return JsonResponse({'message':'INVALID_PRODUCT'}, status=401)
 
            if not Like.objects.filter(user_id = user.id, product_id = product_id).exists():
                Like.objects.create(user_id = user.id, product_id = product_id)
            
            return JsonResponse({'message':'ADDITION_SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
    @login_decorator
    def delete(self, request, product_id):
        Like.objects.filter(user_id = request.user.id, product_id = product_id).delete()
        
        return JsonResponse({'message':'DELETE_SUCCESS'}, status=204)