from django.shortcuts import render, get_object_or_404

from VideoApp.models import Video
# Create your views here.

def video_list(request):
    videos = Video.objects.all()
    return render(request, 'video/Video_list.html', {'videos': videos})

def video_detail(request, pk):
    videos = get_object_or_404(Video, pk=pk)
    return render(request, 'video/Video_detail.html', {'videos': videos})