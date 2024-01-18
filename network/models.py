from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Now


class User(AbstractUser):
    pass


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="author")
    content = models.TextField()
    time = models.DateTimeField(db_default=Now())
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"Posted {self.time.strftime('%b %d %Y, %I:%M %p')} by {self.author}"


class Followers(models.Model):
    followed = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="followed")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="follower")

    def __str__(self):
        return f"{self.follower} follows {self.followed}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="who_liked")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name="post")

    def __str__(self):
        return f"{self.user} likes {self.post}"