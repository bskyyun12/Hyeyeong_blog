from django.contrib import admin
from .models import Calendar, Image, Comment, Friend, ImageComment

admin.site.register(Calendar)
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(ImageComment)
admin.site.register(Friend)
