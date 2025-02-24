from django.contrib import admin

# Register your models here.
from comments.models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'comment', 'created_on', 'published']
    list_editable = ['published',]

admin.site.register(Comment, CommentAdmin)