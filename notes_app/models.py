from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# cоздаёт таблицу со столбцами: user, title, content, tags, created_at, updated_at.
class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь') # при удалении user удаляются все данные
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    tags = models.CharField(max_length=255, blank=True, verbose_name='Теги (через запятую)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'

    # для админки
    # строковое представление, выводит заголовок, имя пользователя
    def __str__(self):
        return f'{self.title} ({self.user.username})'

    # возвращает url для просмотра заметки
    def get_absolute_url(self):
        return reverse('note_list')