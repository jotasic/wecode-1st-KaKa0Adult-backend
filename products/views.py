import json, math
from django.db.models.aggregates import Aggregate
from django.db.models.query_utils import Q

from django.http.response         import JsonResponse
from django.views                 import View
from django.db.models             import Count

from products.models              import Product
from orders.models                import OrderStatus
from users.utils                  import login_decorator

class ProductView(View):
    @login_decorator
    def get(self, request):
        user             = request.user
        product_type     = request.GET.get('type')
        character        = request.GET.get('character')
        search           = request.GET.get('search')
        category         = request.GET.get('category')
        page             = int(request.GET.get('page', 0))
        page_size        = int(request.GET.get('pageSize', 0))
        order_conditions = []
        q                = Q()
        result           = {}

        if product_type == 'hot':
            order_conditions.append('-count')

        if category:
            q |= Q(category__name__icontains=category)

        if character:
            q |= Q(character__name__icontains=character)

        if search:
            q |= Q(name__icontains=search)

        order_conditions.append('-created_at')
        
        filtered_products = Product.objects.filter(
            q).annotate(count=Count("like__product_id")).order_by(
                *order_conditions)
        
        total_count = filtered_products.count()

        if page > 0 or page_size > 0:
            started_idx       = (page - 1) * page_size
            ended_idx         = started_idx + page_size
            filtered_products = filtered_products[started_idx:ended_idx]

            result['page']           = page
            result['pageSize']       = page_size
            result['totalPageCount'] = math.ceil(total_count / page_size)

        result['totalCount']       = total_count
        result['numberOfElements'] = filtered_products.count()
        result['resultList']       = [{
            'id'    : product.id,
            'name'  : product.name,
            'price' : product.price,
            'stock' : product.stock,
            'like'  : product.user_set.filter(id=user.id).exists(),
            'cart'  : product.orderitem_set.filter(
                order__user=user,
                order__order_status__status=OrderStatus.BASKET).exists(),
            'image' : product.imageurl_set.order_by('id')[0].url
                } for product in filtered_products]
                
        return JsonResponse(result, status=200)