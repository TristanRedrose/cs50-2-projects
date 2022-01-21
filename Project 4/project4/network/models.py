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
