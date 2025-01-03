
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newPost" , views.new_post , name="newPost"),
    path("profile/<int:uid>", views.profile, name="profile"),
    path("follow", views.follow, name="follow"),
    path("unfollow", views.unfollow, name="unfollow"), 
    path("edit/<int:pid>", views.edit, name="edit"), 
    path("like/<int:pid>", views.like_post, name="like"),
]
