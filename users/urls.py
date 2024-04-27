from django.urls import path
from . import views


app_name = "users"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("get_user/", views.get_user, name="get_user"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("change_password/", views.change_password, name="change_password"),
]
