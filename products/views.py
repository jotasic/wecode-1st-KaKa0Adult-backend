from django.http.response        import Http404, JsonResponse
from django.views                import View
from django.db.models            import Value
from django.db.models.functions  import Coalesce
from django.db.models.aggregates import Count, Avg
from django.shortcuts            import get_object_or_404

from products.models             import Product
from orders.models               import OrderStatus
from users.utils                 import login_decorator

class ProductDetailView(View):
    @login_decorator
    def get(self, request, product_id):
        try:
            product = get_object_or_404(Product, id=product_id)
            user    = request.user

            sart_point = product.review_set.aggregate(
                    avg=Coalesce(Avg('star_point'), Value(0.0)),
                    count=Count('id'))

            result  = {
                'id'             : product.id,
                'name'           : product.name,
                'price'          : product.price,
                'content'        : product.content,
                'stock'          : product.stock,
                'starPoint'      : sart_point['avg'],
                'starPointCount' : sart_point['count'],
                'imageUrls'      : list(
                    product.imageurl_set.values_list(
                    'url', flat=True).order_by('id')),
                'like'           : product.user_set.filter(id=user.id).exists(),
                'cart'           : product.orderitem_set.filter(
                    order__user                 = user,
                    order__order_status__status = OrderStatus.BASKET).exists(),
            }

            return JsonResponse(result, status=200)

        except Http404:
            return JsonResponse({'message':'PRODUCT_NOT_FOUND'}, status=404)