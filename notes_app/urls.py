from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('notes/', views.note_list, name='note_list'),
#     path('notes/search/', views.note_search, name='note_search'),
#     path('notes/create/', views.note_create, name='note_create'),
#     path('notes/edit/<int:pk>/', views.note_edit, name='note_edit'),
#     path('notes/delete/<int:pk>/', views.note_delete, name='note_delete'),
#     path('register/', views.register, name='register'),
# ]

urlpatterns = [
    path('', views.note_list, name='note_list'),  # список заметок
    path('search/', views.note_search, name='note_search'),
    path('create/', views.note_create, name='note_create'),
    path('edit/<int:pk>/', views.note_edit, name='note_edit'),
    path('delete/<int:pk>/', views.note_delete, name='note_delete'),
    path('register/', views.register, name='register'),
    # убрала login/logout (они в accounts/)
]