from django.contrib import admin
from .models import Post, TTUser, Comment


# Register your models here.
admin.site.register(Post)
admin.site.register(TTUser)
admin.site.register(Comment)
