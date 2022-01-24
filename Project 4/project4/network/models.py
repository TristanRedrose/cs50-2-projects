from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Posts(models.Model):
    writer = models.ForeignKey("User", on_delete=models.CASCADE, related_name="writer")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes= models.IntegerField(default= 0)

    def serialize(self):
        return {
            "id": self.id,
            "writer": self.writer.username,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b. %d, %Y, %I:%M %p"),
            "likes": self.likes
        }

    class Meta:
        verbose_name= "Post"
        verbose_name_plural= "Posts"

class Following(models.Model):
    follower = models.ForeignKey("User", on_delete=models.CASCADE, unique=True, related_name="follower")
    following = models.ManyToManyField("User", related_name="followers")
    followers = models.PositiveIntegerField(default=0)

class Liked(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, unique=True, related_name="viewer")
    liked = models.ManyToManyField("Posts", related_name="liked")

