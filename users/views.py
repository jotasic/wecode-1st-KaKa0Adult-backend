import json, bcrypt, jwt

from django.views            import View
from django.http             import JsonResponse
from rest_framework          import generics

from products.models         import Product
from .models                 import User, Like
from users.utils             import login_decorator
from kaka0Adult.settings     import SECRET_KEY, ALGORITHM
from .serializers            import UserSerializer

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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
    
    @login_decorator
    def get(self, request):
        result = {
            'product_list'  :[{
                'id'        : product.id,
                'name'      : product.name,
                'image_url' : product.imageurl_set.order_by('id')[0].url
            } for product in request.user.like.all()]
        }
        return JsonResponse(result, status=200)