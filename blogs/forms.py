from .models import Comment, Post, Images
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content')

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label= 'Image')
    class Meta:
        model = Images
        fields = ('image',)