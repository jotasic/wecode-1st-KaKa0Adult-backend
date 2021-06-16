from django.urls import path

from .views import BasketView, OrderView

urlpatterns = [
    path('/order-items/<int:order_item>', BasketView.as_view()),
    path('/order-items', BasketView.as_view()),
    path('', OrderView.as_view())
]
