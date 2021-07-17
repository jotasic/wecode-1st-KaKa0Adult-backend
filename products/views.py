import math

from django.http.response         import Http404, JsonResponse
from django.views                 import View
from django.db.models             import Count, Avg, Q, Exists
from django.shortcuts             import get_object_or_404

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

class ProductListView(View):
    @login_decorator
    def get(self, request):
        order_conditions = {
            'new'       : '-created_at',
            'old'       : 'created_at',
            'popular'   : '-count',
            'unpopular' : 'count',
            'highPrice' : '-price',
            'lowPrice'  : 'price',
            'bestSell'  : '-sell_count',
            'worstSell' : 'sell_count'
        }

        user      = request.user
        character = request.GET.get('character')
        search    = request.GET.get('search')
        category  = request.GET.get('category')
        order     = request.GET.get('order', '')
        page      = int(request.GET.get('page', 0))
        page_size = int(request.GET.get('pageSize', 0))
        q         = Q()
        
        if category:
            q &= Q(category__name__icontains=category)

        if character:
            q &= Q(character__name__icontains=character)

        if search:
            q &= Q(name__icontains=search)

        filtered_products = Product.objects.filter(
            q).select_related('category', 'character').prefetch_related('imageurl_set', 'user_set', 'orderitem_set__order').annotate(count=Count('like__product_id')).order_by(
                order_conditions.get(order, 'id'))
        
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
                    order__order_status_id = OrderStatus.BASKET).select_related('order').exists(),
                'image' : product.imageurl_set.all()[0].url
                } for product in filtered_products]
        }

        return JsonResponse(result, status=200)