from django.views.generic import (
    DetailView,
    View,
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
)

from blog.forms import PostModelForm
from blog.models import Post


class PostGenericDetailView(DetailView):
    model = Post


class PostGenericListView(ListView):
    model = Post


class PostGenericUpdateView(UpdateView):
    model = Post
    fields = ["author", "title", "content"]


class PostGenericCreateView(CreateView):
    model = Post
    form_class = PostModelForm
    template_name = "blog/generics/create_post.html"


class PostGenericDeleteView(DeleteView):
    model = Post
