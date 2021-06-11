import json
from json.decoder import JSONDecodeError

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from .models         import Order, OrderStatus, OrderList
from users.models    import User 
from products.models import Product

class BasketView(View):
    def post(self, request, product_id):
        try:
            data = json.loads(request.body)

            product_count = data['count']

            product      = Product.objects.get(id=product_id)
            user         = User.objects.get(id=4)
            order_status = OrderStatus.objects.get(status='BASKET')
            
            order, created = Order.objects.get_or_create(
                user=user, order_status=order_status,
                defaults={
                    'user':user, 
                    'order_status':order_status,
                } 
            )
            # 트렌잭션 처리 질문하기 
            # if OrderList.objects.filter(product=product, order=order).exists():
            #     return JsonResponse({'message':'PRODUCT_EXISTS'}, status=400)
                
            OrderList.objects.create(product=product, order=order, count=product_count)

            return JsonResponse({'message':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        except MultipleObjectsReturned:
            return JsonResponse({'message':'MULTIPLE_OBJECT_RETURNED'}, status=500)
        
        except ObjectDoesNotExist:
            return JsonResponse({'message':'DOES_NOT_EXIST'}, status=401)

        except JSONDecodeError:
            return JsonResponse({'message':'DECODE_ERROR'}, status=40)
 
    def delete(self, request, product_id):
        try:
            product      = Product.objects.get(id=product_id)
            user         = User.objects.get(id=4)
            order_status = OrderStatus.objects.get(status='BASKET')

            order = Order.objects.get(user=user, order_status=order_status)

            OrderList.objects.get(order=order, product=product).delete()

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except MultipleObjectsReturned:
            return JsonResponse({'message':'MULTIPLE_OBJECT_RETURNED'}, status=500)

        except ObjectDoesNotExist:
            return JsonResponse({'message':'DOES_NOT_EXIST'}, status=401)
