from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.views.generic import DetailView, View

from blog.forms import PostForm, CommentForm, PostModelForm, CommentModelForm
from blog.models import Post, Comment

User = get_user_model()

"""
Mając zapisane w bazie pewną pulę postów, chcemy zrobić końcówkę(url) po wejściu na który wyświetli nam się lista takich postów

Pamiętajcie o tym jak do tej pory robiliśmy widoki, a z nowych rzeczy to jak pobieraliśmy z bazy rekordy dotyczące postów, 
google i docsy django też tutaj będą na pewno w stanie pomóc
"""


def get_posts(request):
    posts = Post.objects.all()
    ctx = {"posts": posts}

    return render(request, "blog/posts.html", context=ctx)


def get_post(request, id: int):
    """
    Co chcemy zmienić: chcemy ten widok usprawnić, aby w momencie podania id po którym nie znajdujemy posta, nie wywalał się błąd,
    a user dostanie informację, że taki post nie istnieje
    """
    try:
        post = Post.objects.get(id=id)
        ctx = {"post": post}

    except Post.DoesNotExist:
        ctx = {"post_id": id}

    return render(request, "blog/post.html", context=ctx)


def get_comments(request):
    comments = Comment.objects.all()
    ctx = {"comments": comments}

    return render(request, "blog/comments.html", context=ctx)


def get_comment(request, id: int):
    try:
        comment = Comment.objects.get(id=id)
        ctx = {"comment": comment}
    except Comment.DoesNotExist:
        ctx = {"comment_id": id}

    return render(request, "blog/comment.html", context=ctx)


@login_required
def create_post(request):
    if request.method == "GET":
        form = PostModelForm()
        ctx = {"form": form}
        return render(request, "blog/create_post.html", context=ctx)
    elif request.method == "POST":
        form = PostModelForm(data=request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            author = request.user
            post.author = author
            post.save()
            ctx = {"post": post, "form": form}
            return render(request, "blog/create_post.html", context=ctx)
        return render(request, "blog/create_post.html", {"form": form})


def create_comment(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            ctx = {"not_authenticated": True}
            return render(request, "blog/create_comment.html", context=ctx)
        form = CommentModelForm()
        ctx = {"form": form}
        return render(request, "blog/create_comment.html", context=ctx)
    elif request.method == "POST":
        form = CommentModelForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            author = request.user
            comment.author = author
            comment.save()
            ctx = {"comment": comment, "form": form}

            return render(request, "blog/create_comment.html", context=ctx)
        return render(request, "blog/create_comment.html", {"form": form})


class PostListView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        ctx = {"posts": posts}

        return render(self.request, "blog/posts.html", context=ctx)


class PostDetailView(View):
    def get(self, request, id, *args, **kwargs):
        try:
            post = Post.objects.get(id=id)
            ctx = {"post": post}
        except Post.DoesNotExist:
            ctx = {"post_id": id}

        return render(self.request, "blog/post.html", context=ctx)


class CommentListView(View):
    def get(self, request, *args, **kwargs):
        comments = Comment.objects.all()
        ctx = {"comments": comments}

        return render(self.request, "blog/comments.html", context=ctx)


class CommentDetailView(View):
    def get(self, request, id, *args, **kwargs):
        try:
            comment = Comment.objects.get(id=id)
            ctx = {"comment": comment}
        except Comment.DoesNotExist:
            ctx = {"comment_id": id}

        return render(self.request, "blog/comment.html", context=ctx)


class PostCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = PostModelForm()
        ctx = {"form": form}

        return render(request, "blog/create_post.html", context=ctx)

    def post(self, request, *args, **kwargs):
        form = PostModelForm(data=request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            author = request.user
            post.author = author
            post.save()
            ctx = {"post": post, "form": form}
            return render(request, "blog/create_post.html", context=ctx)
        return render(request, "blog/create_post.html", {"form": form})


class CommentCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = CommentModelForm()
        ctx = {"form": form}

        return render(request, "blog/create_comment.html", context=ctx)

    def post(self, request, *args, **kwargs):
        form = CommentModelForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            author = request.user
            comment.author = author
            comment.save()
            ctx = {"comment": comment, "form": form}

            return render(request, "blog/create_comment.html", context=ctx)
        return render(request, "blog/create_comment.html", {"form": form})


class PostUpdateView(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        try:
            post = Post.objects.get(id=id, author=request.user)
        except Post.DoesNotExist:
            ctx = {"post_id": id, "errors": True}
            return render(request, "blog/post_update.html", context=ctx)

        form = PostModelForm(instance=post)
        ctx = {"form": form, "post": post}

        return render(request, "blog/post_update.html", context=ctx)

    def post(self, request, id, *args, **kwargs):  # normalnie aktualizujemy patch/put, ale formularz w html pozwala nam na post/get
        try:
            post = Post.objects.get(id=id, author=request.user)
        except Post.DoesNotExist:
            return HttpResponseBadRequest()
        form = PostModelForm(data=request.POST)
        if form.is_valid():
            post.content = form.cleaned_data["content"]
            post.title = form.cleaned_data["title"]
            post.save(update_fields=["content", "title"])
            ctx = {"form": form, "post": post}

            return render(request, "blog/post_update.html", context=ctx)

        ctx = {"errors": form.errors}
        return render(request, "blog/post_update.html", context=ctx)


class CommentUpdateView(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        try:
            comment = Comment.objects.get(id=id, author=request.user)
        except Comment.DoesNotExist:
            ctx = {"comment_id": id, "errors": True}
            return render(request, "blog/comment_update.html", context=ctx)

        form = CommentModelForm(instance=comment)
        ctx = {"form": form, "comment": comment}

        return render(request, "blog/comment_update.html", context=ctx)

    def post(self, request, id, *args, **kwargs):  # normalnie aktualizujemy patch/put, ale formularz w html pozwala nam na post/get
        try:
            comment = Comment.objects.get(id=id, author=request.user)
        except Comment.DoesNotExist:
            return HttpResponseBadRequest()
        form = CommentModelForm(data=request.POST)
        if form.is_valid():
            comment.post = form.cleaned_data["post"]
            comment.content = form.cleaned_data["content"]
            comment.save(update_fields=["post", "content"])
            ctx = {"form": form, "comment": comment}

            return render(request, "blog/comment_update.html", context=ctx)
        ctx = {"errors": form.errors}
        return render(request, "blog/comment_update.html", context=ctx)


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        try:
            post = Post.objects.get(id=id, author=request.user)
        except Post.DoesNotExist:
            ctx = {'post_id': id, 'errors': True}
            return render(request, "blog/post_delete.html", context=ctx)
        post_title = post.title
        post_id = post.id
        post.delete()

        ctx = {"is_deleted": True, "post": {"post_title": post_title, "post_id": post_id}}

        return render(request, "blog/post_delete.html", context=ctx)


class CommentDeleteView(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        try:
            comment = Comment.objects.get(id=id, author=request.user)
        except Comment.DoesNotExist:
            ctx = {'comment_id': id, 'errors': True}
            return render(request, "blog/comment_delete.html", context=ctx)

        comment_content = comment.content
        comment_id = comment.id
        comment.delete()

        ctx = {"is_deleted": True, "comment": {"content": comment_content, "id": comment_id}}

        return render(request, "blog/comment_delete.html", context=ctx)
