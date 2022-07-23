from django.contrib import admin
from django.urls import path, include

from first_app.views import (
    hello_world,
    flatten_list,
    flatten_list_with_html,
    my_next_view_with_context,
    iterate_over_months,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("hello_world/", hello_world),
    path("flatten_list/", flatten_list),
    path("flatten_list_html/", flatten_list_with_html),
    path("view_with_ctx/", my_next_view_with_context),
    path("months", iterate_over_months),
    path("blog/", include("blog.urls"), name="blog"),
    path("generic-blog/", include("blog.generic_urls", namespace="generic_blog"), name="generic_blog"),
]
