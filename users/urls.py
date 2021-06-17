from django.urls import path

from .views import LoginView, SignupView, LikeView

urlpatterns = [
    path('/signup', SignupView.as_view()),
    path('/login', LoginView.as_view()),
    path('/like/product/<int:product_id>', LikeView.as_view()),
    path('/like/product', LikeView.as_view()),
]