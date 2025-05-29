from django.urls import path
from VideoApp import views
from VideoApp.views import register_view, login_view, logout_view ,search_videos

urlpatterns = [
    path('', views.video_list, name='video_list'),
    path('video/<int:pk>/', views.video_detail, name='video_detail'),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('search/', search_videos, name='search_videos'),
    path('playlists/', views.playlist_list, name='playlist_list'),
    path('playlists/create/', views.playlist_create, name='playlist_create'),
    path('playlists/<int:pk>/', views.playlist_detail, name='playlist_detail'),
    path('video/<int:video_id>/add-to-playlist/', views.add_to_playlist, name='add_to_playlist'),
    path('playlists/<int:playlist_id>/remove-video/<int:video_id>/', views.remove_from_playlist, name='remove_from_playlist'),
]