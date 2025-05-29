from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from VideoApp.models import Comment
from .models import Playlist

class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]        

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['text']

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }