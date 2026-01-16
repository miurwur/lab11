from django.contrib import admin
from .models import Note

# отображение заметок для админа
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at', 'tags']
    list_filter = ['created_at', 'user']
    search_fields = ['title', 'content', 'tags']