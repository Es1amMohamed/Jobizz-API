from django.urls import path
from . import views
from .views import *

app_name = "users"

urlpatterns = [
    path("signup/", UserSignUpView.as_view(), name="signup"),
    path("login/", views.login, name="login"),
    path("change_password/", views.change_password, name="change_password"),
    path("user/", views.get_user, name="get_user"),
    path("company/<int:pk>/", views.get_company_profile, name="get_company"),
]
