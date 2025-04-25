from django.shortcuts import render, get_object_or_404

from VideoApp.models import Video
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
# Create your views here.

def video_list(request):
    videos = Video.objects.all()
    return render(request, 'video/Video_list.html', {'videos': videos})

def video_detail(request, pk):
    videos = get_object_or_404(Video, pk=pk)
    return render(request, 'video/Video_detail.html', {'videos': videos})




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