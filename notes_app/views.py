from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models import Q

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm


from .forms import CustomUserCreationForm, NoteForm
from .models import Note


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматически входим после регистрации
            return redirect('note_list')
        else:
            messages.error(request, 'Исправьте ошибки в форме')
    else:
        form = CustomUserCreationForm()

    return render(request, 'notes_app/register.html', {'form': form})


def home(request):
    """Главная страница со всеми пользователями"""
    users = User.objects.annotate(
        notes_count=Count('note')
    ).order_by('-notes_count')
    return render(request, 'notes_app/home.html', {'users': users})


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('note_list')
    else:
        form = AuthenticationForm()

    return render(request, 'notes_app/login.html', {'form': form})


def custom_logout(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('home')

@login_required
def note_list(request):
    """Список заметок текущего пользователя"""
    notes = Note.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notes_app/note_list.html', {'notes': notes})


@login_required
def note_edit(request, pk):
    """Редактирование существующей заметки"""
    note = get_object_or_404(Note, pk=pk, user=request.user)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Заметка обновлена!')
            return redirect('note_list')
    else:
        form = NoteForm(instance=note)

    return render(request, 'notes_app/note_form.html', {'form': form})


@login_required
def note_delete(request, pk):
    """Удаление заметки"""
    note = get_object_or_404(Note, pk=pk, user=request.user)

    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Заметка удалена!')
        return redirect('note_list')

    return render(request, 'notes_app/note_confirm_delete.html', {'note': note})


@login_required
def note_create(request):
    """Создание новой заметки"""
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, 'Заметка создана!')
            return redirect('note_list')
    else:
        form = NoteForm()

    return render(request, 'notes_app/note_form.html', {'form': form})



@login_required
def note_search(request):
    """Поиск заметок по ключевым словам и тегам"""
    query = request.GET.get('q', '')

    notes = Note.objects.filter(user=request.user)

    if query:
        notes = notes.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__icontains=query)
        )

    return render(request, 'notes_app/note_list.html', {
        'notes': notes,
        'search_query': query
    })