from django.http.response        import Http404, JsonResponse
from django.views                import View
from django.db.models            import Value
from django.db.models.functions  import Coalesce
from django.db.models.aggregates import Avg
from django.shortcuts            import get_object_or_404

from products.models             import Product
from users.utils                 import login_decorator

class ProductDetailView(View):
    @login_decorator
    def get(self, request, product_id):
        try:
            product = get_object_or_404(Product, id=product_id)
            user    = request.user
            result  = {
                'id'        : product.id,
                'name'      : product.name,
                'price'     : float(product.price),
                'content'   : product.content,
                'stock'     : product.stock > 0,
                'starPoint' : product.review_set.aggregate(
                    avg=Coalesce(Avg('star_point'), Value(0.0)))['avg'],
                'imageUrls' : list(
                    product.imageurl_set.values_list(
                    'url', flat=True).order_by('id')),
                'like'      : product.user_set.filter(id=user.id).exists(),
                'cart'      : product.orderlist_set.all().filter(
                    order__user__id             = user.id,
                    order__order_status__status = 'BASKET').exists(),
            }

            return JsonResponse(result, status=200)

        except Http404:
            return JsonResponse({'message':'PRODUCT_NOT_FOUND'}, status=404)