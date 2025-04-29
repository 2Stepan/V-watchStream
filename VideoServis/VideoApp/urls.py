from django.urls import path
from VideoApp import views
from django.urls import path
from VideoApp.views import register_view, login_view, logout_view ,search_videos

urlpatterns = [
    path('', views.video_list, name='video_list'),
    path('video/<int:pk>/', views.video_detail, name='video_detail'),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('search/', search_videos, name='search_videos'),
]