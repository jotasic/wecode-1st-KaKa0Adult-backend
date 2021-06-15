from django.urls import path

from .views import BasketView

urlpatterns = [
    path('/order-item', BasketView.as_view()),
    path('/order-items/<int:order_item>', BasketView.as_view()),
    path('/order-items', BasketView.as_view()),
]
