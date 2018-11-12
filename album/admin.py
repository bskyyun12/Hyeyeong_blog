from django.contrib import admin
from .models import Calendar, Image, Comment, Friend, ImageComment, Notification, YunList

admin.site.register(Calendar)
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(ImageComment)
admin.site.register(Friend)
admin.site.register(YunList)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'post', 'post_comment', 'image', 'image_comment', 'like', 'date')
admin.site.register(Notification, NotificationAdmin)
