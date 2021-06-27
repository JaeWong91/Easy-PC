from django.contrib import admin
from .models import Post, Comment


admin.site.register(Post)
admin.site.register(Comment)


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
    )
