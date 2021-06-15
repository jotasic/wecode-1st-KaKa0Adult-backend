from django.urls import path

from .views import LoginView, SignupView, DeleteAccount

urlpatterns = [
    path('/signup', SignupView.as_view()),
    path('/login', LoginView.as_view()),
    path('/account', DeleteAccount.as_view()),
]