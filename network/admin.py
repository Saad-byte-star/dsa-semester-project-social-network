from django.contrib import admin
from .models import Post , User , Follower , Like
# Register your models here.
admin.site.register(Post)
admin.site.register(User)
admin.site.register(Follower)
admin.site.register(Like)
