
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),    
    path("following", views.following, name="following"),
    path("profile/<str:username>", views.profile, name="profile"),    
    path("follow", views.follow, name="follow"),
    path("unfollow", views.unfollow, name="unfollow"),

    path("posts", views.create, name="create"),
    path("likes", views.likes, name="likes"),
    path("unlike", views.unlike, name="unlike"),
    path("edit", views.edit, name="edit"),
]
