from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse

from VideoApp.models import Video, Comment, Like, VideoView
from VideoApp.forms import CommentForm, RegisterForm

# Create your views here.


def video_list(request):
    videos = Video.objects.all()
    return render(request, "video/Video_list.html", {"videos": videos})


def video_detail(request, pk):
    video = get_object_or_404(Video, pk=pk)
    comments = video.comments.all()
    form = CommentForm(request.POST or None)
    liked = (
        request.user.is_authenticated
        and Like.objects.filter(video=video, user=request.user).exists()
    )

    # Получение рекомендованных видео
    recommended_videos = Video.objects.exclude(pk=pk).order_by("?")[:5]

    # Добавляем запись в историю просмотров, если пользователь аутентифицирован
    if request.user.is_authenticated:
        VideoView.objects.get_or_create(video=video, user=request.user)

    if "comment_submit" in request.POST and form.is_valid():
        comment = form.save(commit=False)
        comment.video = video
        comment.author = request.user
        comment.save()
        return redirect("video_detail", pk=video.pk)

    elif "like_submit" in request.POST and request.user.is_authenticated:
        like, created = Like.objects.get_or_create(video=video, user=request.user)
        if not created:
            like.delete()
        return redirect("video_detail", pk=video.pk)

    context = {
        "video": video,
        "comments": comments,
        "form": form,
        "liked": liked,
        "recommended_videos": recommended_videos,
    }
    return render(request, "video/video_detail.html", context)


# авторизация


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
    search_query = request.GET.get("q", "")
    hashteg_filter = request.GET.get("hashteg", "")

    videos = Video.objects.all()

    if search_query:
        videos = videos.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    if hashteg_filter:
        videos = videos.filter(hashteg__iexact=hashteg_filter)

    all_hashtegs = (
        Video.objects.exclude(Q(hashteg__isnull=True) | Q(hashteg__exact=""))
        .values_list("hashteg", flat=True)
        .distinct()
    )

    return render(
        request,
        "video/Video_list.html",
        {
            "videos": videos,
            "all_hashtegs": all_hashtegs,
            "search_query": search_query,
            "current_hashteg": hashteg_filter,
        },
    )


# понравившееся
def like_videos(request):
    liked_videos = Like.objects.filter(user=request.user).select_related('video')
    videos = [lv.video for lv in liked_videos]
    return render(request, 'video/liked_videos.html', {'videos': videos})

def history_videos(request):
    viewed_videos = VideoView.objects.filter(user=request.user).select_related('video').order_by('-viewed_at')
    return render(request, 'video/history_videos.html', {'viewed_videos': viewed_videos})
