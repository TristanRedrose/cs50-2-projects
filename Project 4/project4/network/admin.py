from django.contrib import admin

# Register your models here.
from .models import Posts, Following

admin.site.register(Posts)
admin.site.register(Following)
