from django.urls import path
from . import views


app_name = 'chadeo'

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("signup", views.create_user , name="create_user")
]