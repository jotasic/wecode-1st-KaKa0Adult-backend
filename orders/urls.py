from django.urls import path

from .views import BasketView

urlpatterns = [
    path('/basket/product/<int:product_id>', BasketView.as_view())
]
