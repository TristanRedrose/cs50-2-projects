from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator



class User(AbstractUser):
    pass

class Categories(models.Model):
    cat = models.CharField(max_length=32, unique=True, blank=False, default=None)

    class Meta:
        verbose_name= "Category"
        verbose_name_plural= "Categories"

    def __str__(self):
        return f"{self.cat}"

class Listings(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    title = models.CharField(max_length=100, blank=False, default=None)
    description = models.CharField(max_length=300, blank=False, default=None)
    ctg = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name= "category")
    picture = models.URLField(blank=True)
    bid = models.IntegerField(validators=[MinValueValidator(0)])
    time = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name= "Listing"
        verbose_name_plural= "Listings"

    def __str__(self):
        return f"{self.id}:{self.title} creator:{self.creator} category:{self.ctg} bid:{self.bid} created {self.time} active:{self.active}"
