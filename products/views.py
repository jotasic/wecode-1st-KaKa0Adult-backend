import math
from django.db.models.query_utils import Q

from django.http.response         import Http404, JsonResponse
from django.views                 import View
from django.db.models             import Count, Avg
from django.shortcuts            import get_object_or_404

from products.models              import Product
from orders.models                import OrderStatus
from users.utils                  import login_decorator

class ProductDetailView(View):
    @login_decorator
    def get(self, request, product_id):
        try:
            product = get_object_or_404(Product, id=product_id)
            user    = request.user

            sart_point = product.review_set.aggregate(
                    avg=Avg('star_point'), count=Count('id'))

            result  = {
                'id'             : product.id,
                'name'           : product.name,
                'price'          : product.price,
                'content'        : product.content,
                'stock'          : product.stock,
                'starPoint'      : sart_point['avg'] if sart_point['avg'] else 0.0,
                'starPointCount' : sart_point['count'],
                'imageUrls'      : list(
                    product.imageurl_set.values_list(
                    'url', flat=True).order_by('id')),
                'like'           : product.user_set.filter(id=user.id).exists(),
                'cart'           : product.orderitem_set.filter(
                    order__user            = user,
                    order__order_status_id = OrderStatus.BASKET).exists(),
            }

            return JsonResponse(result, status=200)

        except Http404:
            return JsonResponse({'message':'PRODUCT_NOT_FOUND'}, status=404)

class ProductView(View):
    @login_decorator
    def get(self, request):
        order_columns = {
            'createdAt' : 'created_at',
            'like'      : 'count',
            'price'     : 'price',
        }

        order_sort = {
            'desc' : '-',
            'asc'  : ''
        }

        user      = request.user
        character = request.GET.get('character')
        search    = request.GET.get('search')
        category  = request.GET.get('category')
        order     = request.GET.get('order')
        page      = int(request.GET.get('page', 0))
        page_size = int(request.GET.get('pageSize', 0))
        q         = Q()
        result    = {}

        conditions = {
            'category'  : Q(category__name__icontains=category),
            'character' : Q(character__name__icontains=character),
            'search'    : Q(name__icontains=search)
        }

        if category:
            q &= conditions['category']

        if character:
            q &= conditions['character']

        if search:
            q &= conditions['search']

        if order:
            order = order.split(',')
            order = order_sort[order[1]]+order_columns[order[0]]

        filtered_products = Product.objects.filter(
            q).annotate(count=Count("like__product_id")).order_by(
                order)
        
        total_count = filtered_products.count()

        if page > 0 or page_size > 0:
            started_idx       = (page - 1) * page_size
            ended_idx         = started_idx + page_size
            filtered_products = filtered_products[started_idx:ended_idx]

        result = {   
            'totalCount'      : total_count,
            'numberOfElements': filtered_products.count(),
            'page'            : page,
            'pageSize'        : page_size,
            'totalPageCount'  : math.ceil(total_count / page_size) if page_size > 0 else 0,
            'resultList'      : [{
                'id'    : product.id,
                'name'  : product.name,
                'price' : product.price,
                'stock' : product.stock,
                'like'  : product.user_set.filter(id=user.id).exists(),
                'cart'  : product.orderitem_set.filter(
                    order__user            = user,
                    order__order_status_id = OrderStatus.BASKET).exists(),
                'image' : product.imageurl_set.order_by('id')[0].url
                } for product in filtered_products]
        }
                
        return JsonResponse(result, status=200)