from django.contrib import admin

from .models import User, Categories, Listings, Comment, Watchlist, Bidding

# Register your models here.
class ListAdmin(admin.ModelAdmin):
    list_display = ("id", "creator", "title", "description", "ctg", "bid", "time", "active")

class CommAdmin(admin.ModelAdmin):
    list_display = ("id", "writer", "subject", "comment")

admin.site.register(User)
admin.site.register(Categories)
admin.site.register(Listings, ListAdmin)
admin.site.register(Comment, CommAdmin)
admin.site.register(Watchlist)
admin.site.register(Bidding)