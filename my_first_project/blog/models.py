from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models

User = AUTH_USER_MODEL

"""
Post

id: int  # dostajemy od ręki w Django
author: FK 
title: CharField
content: TextField
created_at: Datetime
updated_at: Datetime
"""


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="Some default title")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post by: {self.author}, created at: {self.created_at}"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment {self.id} by: {self.author}, for Post {self.post.title}"


class Reaction(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, default=None)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True, default=None)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reaction id: {self.id}"


"""
Co zrobić:
do modelu reaction chcemy dodać widoki, templatki oraz urle które pozwolą nam lajkować posty oraz komentarze, trzeba
pamiętać, że w danym momencie możemy dodać reakcję tylko dla komentarza, lub postu. Liczba lajków powinna się wyświetlać zarówno
w detailu posta i komentarza jak i w widokach listy, tam też powinny być opcje zalajkowania danego posta i komentarza.

Pamiętajcie o tym by wyświetlać odpowiednie komunikaty dla usera w momencie, gdy wprowadził coś nie tak, czy też program
nie zadziałał jak należy
"""