from django.contrib import admin 
from .models import Like , User,Post,Follow

# Register your models here.
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(User)
admin.site.register(Follow)