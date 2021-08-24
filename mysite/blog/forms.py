from django import forms
from .models import Post
from django.forms.widgets import FileInput


class PostForm(forms.ModelForm):
    image_file = forms.FileField(widget=FileInput)
    class Meta:
        model = Post
        fields = ('title', 'text','image_file',)