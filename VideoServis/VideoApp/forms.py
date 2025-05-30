from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from VideoApp.models import Comment

class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]        

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': '',  # Установка пустой метки
        }

        
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['placeholder'] = 'Введите ваш комментарий...'