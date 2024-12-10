from django.contrib import admin
from .models import Event, File, Message

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'description')
@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['file', 'user', 'title', 'event', 'description', 'uploaded_at']
    search_fields = ['title', 'description', 'keywords']
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['event', 'user', 'message', 'uploaded_at']
    search_fields = ['event', 'user']
    