from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Playlist, PlaylistVideo
from .forms import PlaylistForm

from VideoApp.models import Video, Comment, Like
from VideoApp.forms import CommentForm, RegisterForm
# Create your views here.

def video_list(request):
    videos = Video.objects.all()
    return render(request, 'video/Video_list.html', {'videos': videos})

def video_detail(request, pk):
    video = get_object_or_404(Video, pk=pk)
    comments = video.comments.all()
    form = CommentForm(request.POST or None)
    liked = request.user.is_authenticated and Like.objects.filter(video=video, user=request.user).exists()

    if 'comment_submit' in request.POST and form.is_valid():
        comment = form.save(commit=False)
        comment.video = video
        comment.author = request.user
        comment.save()
        return redirect('video_detail', pk=video.pk)

    elif 'like_submit' in request.POST and request.user.is_authenticated:
        like, created = Like.objects.get_or_create(video=video, user=request.user)
        if not created:
            like.delete()
        return redirect('video_detail', pk=video.pk) # redirect после обработки лайка


    context = {'video': video, 'comments': comments, 'form': form, 'liked': liked}
    return render(request, 'video/video_detail.html', context)



#авторизация

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("video_list")  # Перенаправление на главную страницу
    else:
        form = RegisterForm()
    return render(request, "register/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("video_list")  # Перенаправление на главную страницу
    else:
        form = AuthenticationForm()
    return render(request, "register/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")

def video_list_view(request):
    return render(request, "video_list.html")


# коменты и видео


# поиск по названию и хештегам
def search_videos(request):
    search_query = request.GET.get('q', '')
    hashteg_filter = request.GET.get('hashteg', '')

    videos = Video.objects.all()
    
    if search_query:
        videos = videos.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if hashteg_filter:
        videos = videos.filter(hashteg__iexact=hashteg_filter)
        
    all_hashtegs = Video.objects.exclude(
        Q(hashteg__isnull=True) | Q(hashteg__exact='')
    ).values_list('hashteg', flat=True).distinct()
    
    return render(request, 'video/Video_list.html', {
        'videos': videos,
        'all_hashtegs': all_hashtegs,
        'search_query': search_query,
        'current_hashteg': hashteg_filter
    })

# Плейлисты

def playlist_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    playlists = Playlist.objects.filter(owner=request.user)
    return render(request, 'playlist/playlist_list.html', {'playlists': playlists})

def playlist_detail(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk, owner=request.user)
    return render(request, 'playlist/playlist_detail.html', {'playlist': playlist})

def playlist_create(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.owner = request.user
            playlist.save()
            return redirect('playlist_list')
    else:
        form = PlaylistForm()
    return render(request, 'playlist/playlist_form.html', {'form': form})

def add_to_playlist(request, video_id):
    if request.method == 'POST' and request.user.is_authenticated:
        playlist_id = request.POST.get('playlist_id')
        video = get_object_or_404(Video, pk=video_id)
        playlist = get_object_or_404(Playlist, pk=playlist_id, owner=request.user)
        
        # Проверяем, не добавлено ли видео уже в плейлист
        if not PlaylistVideo.objects.filter(playlist=playlist, video=video).exists():
            PlaylistVideo.objects.create(playlist=playlist, video=video)
        
        return redirect('video_detail', pk=video_id)
    return redirect('login')

def remove_from_playlist(request, playlist_id, video_id):
    if request.user.is_authenticated:
        playlist = get_object_or_404(Playlist, pk=playlist_id, owner=request.user)
        video = get_object_or_404(Video, pk=video_id)
        PlaylistVideo.objects.filter(playlist=playlist, video=video).delete()
        return redirect('playlist_detail', pk=playlist_id)
    return redirect('login')