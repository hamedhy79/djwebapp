from django.contrib import admin
from .models import Post, Comment, Vote, PersonSer, Question, Answer, Car


# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug', 'update',)
    search_fields = ('slug', 'body',)
    list_filter = ('created',)
    prepopulated_fields = {'slug': ('body',)}
    raw_id_fields = ('user',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created', 'is_reply')
    raw_id_fields = ('user', 'post', 'reply')


admin.site.register(Vote)
admin.site.register(PersonSer)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Car)