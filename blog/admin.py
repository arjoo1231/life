from django.contrib import admin
from . import models

class CommentInline(admin.StackedInline):
    model = models.Comment
    extra = 0
    
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'updated')
    list_filter = ('status', 'topics')
    search_fields = ('title', 'author__username', 'author__first_name', 'author__last_name')
    inlines = [
        CommentInline,
    ]

class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'approved', 'created', 'post')
    list_filter = ('approved',)
    search_fields = ('name', 'email', 'text')
    list_editable = ('approved',)
    readonly_fields = ('name', 'email', 'text') 




admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Topic, TopicAdmin)
admin.site.register(models.Comment, CommentAdmin)

