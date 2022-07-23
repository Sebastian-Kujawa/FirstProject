from django.urls import path

from blog.views.generic_views import (
    PostGenericCreateView,
    PostGenericDeleteView,
    PostGenericDetailView,
    PostGenericListView,
    PostGenericUpdateView,
)

app_name = "blog"

urlpatterns = [
    path("posts/", PostGenericListView.as_view(), name="post_list"),
    path("posts/<int:id>", PostGenericDetailView.as_view(), name="post_detail"),
    path("create-post", PostGenericCreateView.as_view(), name="post_create"),
    path("update-post", PostGenericUpdateView.as_view(), name="post_update"),
    path("delete-post", PostGenericDeleteView.as_view(), name="post_delete"),
]
