from django.urls import path

from blog.views.views import (
    get_posts,
    get_post,
    create_post,
    get_comments,
    get_comment,
    create_comment,
    PostListView,
    PostDetailView,
    CommentListView,
    CommentDetailView,
    PostCreateView, CommentCreateView, PostUpdateView, CommentUpdateView, PostDeleteView, CommentDeleteView,
)

app_name = "blog"

urlpatterns = [
    # posts
    path("posts/", get_posts, name="post_list"),
    path("posts/<int:id>", get_post, name="post_detail"),
    path("cbv-posts/", PostListView.as_view(), name="cbv_post_list"),
    path("cbv-posts/<int:id>", PostDetailView.as_view(), name="cbv_post_detail"),
    path("create-post", create_post, name="post_create"),
    path("cbv-create-post", PostCreateView.as_view(), name="cbv_post_create"),
    path("cbv-post-update/<int:id>", PostUpdateView.as_view(), name="cbv_post_update"),
    path("cbv-post-delete/<int:id>", PostDeleteView.as_view(), name="cbv_post_delete"),
    # comments
    path("create-comment", create_comment, name="comment_create"),
    path("comments/", get_comments, name="comment_list"),
    path("comments/<int:id>", get_comment, name="comment_detail"),
    path("cbv-comments/", CommentListView.as_view(), name="cbv_comment_list"),
    path(
        "cbv-comments/<int:id>", CommentDetailView.as_view(), name="cbv_comment_detail"
    ),
    path("cbv-create-comment", CommentCreateView.as_view(), name="cbv_comment_create"),
    path("cbv-update-comment/<int:id>", CommentUpdateView.as_view(), name="cbv_comment_update"),
    path("cbv-comment-delete/<int:id>", CommentDeleteView.as_view(), name="cbv_comment_delete"),
]
