from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status',)
    list_filter = ('status',)
    search_fields = ('title', 'content',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('created_by',)
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)