import json, math

from django.http.response         import JsonResponse
from django.views                 import View
from django.db.models             import Count

from products.models              import Product
from users.utils                  import login_decorator

class ProductView(View):
    @login_decorator
    def get(self, request):
        user         = request.user
        product_type = request.GET.get('type', '')
        keyword      = request.GET.get('keyword', '')
        page         = int(request.GET.get('page', 0))
        page_size    = int(request.GET.get('pageSize', 0))
                
        if product_type == 'new':
            filtered_products = Product.objects.order_by('-created_at')

        elif product_type == 'hot':
            filtered_products = Product.objects.annotate(
                count=Count('like__product_id'
                )).order_by('-count', '-id')

        elif product_type == 'category':
            filtered_products = Product.objects.filter(
                category__name__icontains=keyword).order_by('-created_at')

        elif product_type == 'character':
            filtered_products = Product.objects.filter(
                character__name__icontains=keyword).order_by('-created_at')

        elif product_type == 'search':
            filtered_products = Product.objects.filter(
                name__icontains=keyword).order_by('-created_at')

        elif product_type == "":
            filtered_products = Product.objects.all().order_by('-created_at')

        else:
            filtered_products = Product.objects.none()

        total_count          = filtered_products.count()
        result               = {}
        result['totalCount'] = total_count

        if page > 0 and page_size > 0:
            started_idx       = (page - 1) * page_size
            ended_idx         = started_idx + page_size
            filtered_products = filtered_products[started_idx:ended_idx]
            
            result['page']           = page
            result['pageSize']       = page_size
            result['totalPageCount'] = math.ceil(total_count / page_size)
        
        result['numberOfElements'] = filtered_products.count()
        result['resultList']       = [{
            'id'    : product.id,
            'name'  : product.name,
            'price' : product.price,
            'stock' : product.stock > 0,
            'like'  : product.user_set.filter(id=user.id).exists(),
            'cart'  : product.orderlist_set.all().filter(
                order__user__id=user.id,
                order__order_status__status='BASKET').exists(),
            'image' : product.imageurl_set.order_by('id')[0].url
                } for product in filtered_products]
                
        return JsonResponse(result, status=200)