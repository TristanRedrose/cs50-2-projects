from django.contrib import admin

# Register your models here.
from .models import Posts, Following, Liked

admin.site.register(Posts)
admin.site.register(Following)
admin.site.register(Liked)

