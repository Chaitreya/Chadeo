from django.urls import path
from . import views


app_name = 'chadeo'

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_user, name="login_user"),
    path("signup/", views.create_user , name="create_user"),
    path("logout/", views.logout_user, name="logout_user"),
    path("chat/<str:room_name>/",views.chat_room, name="chat_room"),
]