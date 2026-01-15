from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Введите текст заметки'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'работа, учеба, идеи'}),
        }
        labels = {
            'title': 'Заголовок',
            'content': 'Содержание',
            'tags': 'Теги (через запятую)'
        }