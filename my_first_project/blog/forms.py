from django import forms
from django.contrib.auth import get_user_model

from blog.models import Post, Comment

User = get_user_model()


class PostForm(forms.Form):
    author = forms.ModelChoiceField(queryset=User.objects.all())
    title = forms.CharField(max_length=100)
    content = forms.CharField()


class CommentForm(forms.Form):
    author = forms.ModelChoiceField(queryset=User.objects.all())
    post = forms.ModelChoiceField(queryset=Post.objects.all())
    content = forms.CharField()


class PostModelForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={"cols": 20, "rows": 20}))

    class Meta:
        model = Post
        fields = ["title", "content"]


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["post", "content"]
