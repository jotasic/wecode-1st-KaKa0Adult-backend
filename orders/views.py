import json
from json.decoder import JSONDecodeError

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import MultipleObjectsReturned

from .models         import Order, OrderStatus, OrderItem
from products.models import Product
from users.utils     import login_decorator

class BasketView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)

            product       = data['id']            
            product_count = data['count']

            if not Product.objects.filter(id=product).exists():
                return JsonResponse({'message':'PRODUCT_DOES_NOT_EXIST'}, status=400)
            
            order, created = Order.objects.get_or_create(
                user         = request.user,
                order_status = OrderStatus.BASKET
            )

            if OrderItem.objects.filter(product_id=product, order=order).exists():
                return JsonResponse({'message':'EXIST_ITEM'}, status=400)    

            OrderItem.objects.create(product_id=product, order=order, count=product_count)

            return JsonResponse({'message':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        except MultipleObjectsReturned:
            return JsonResponse({'message':'MULTIPLE_OBJECT_RETURNED'}, status=400)

        except JSONDecodeError:
            return JsonResponse({'message':'DECODE_ERROR'}, status=400)

    @login_decorator
    def delete(self, request, order_item):
        if not OrderItem.objects.filter(id=order_item).exists:
            return JsonResponse({'message':'INVALID_ORDER_ITEMS'}, status=400)
            
        order_item = OrderItem.objects.get(id=order_item)

        if order_item.order.user != request.user:
            return JsonResponse({'message':'INVALID_USER'}, status=401)

        if order_item.order.order_status.id != OrderStatus.BASKET:
            return JsonResponse({'message':'ORDER_DOSE_NOT_EXIST'}, status=400)

        order_item.delete()

        return JsonResponse({'message':'SUCCESS'}, status=204)

    @login_decorator
    def patch(self, request):
        try:
            data = json.loads(request.body)

            order_item_id = data['order_item_id']
            count         = data['count']
           
            if count < 0 or type(count) != int:
                return JsonResponse({'message':'INVALID_COUNT_TYPE'})
            
            if not OrderItem.objects.filter(order__user=request.user, id=order_item_id):
                return JsonResponse({'message':'INVALID_ORDER_ITEM'}, status=400)

            OrderItem.objects.filter(id=order_item_id).update(count=count)

            return JsonResponse({'message':'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)