from django.contrib import admin

from blog.models import Comment, Post, Reaction

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reaction)
