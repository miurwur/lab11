"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from notes_app.views import home, register, custom_login, custom_logout

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),  # админка
    path('', home, name='home'),      # главная страница
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('register/', register, name='register'),
    path('notes/', include('notes_app.urls')),
]



# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', home, name='home'),
#     path('login/', auth_views.LoginView.as_view(
#         template_name='notes_app/login.html'
#     ), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(
#         next_page='home'
#     ), name='logout'),
#     path('register/', register, name='register'),
#     path('notes/', include('notes_app.urls')),
# ]

# path(route, view, name=None)  name - "псевдоним" url для удобного обращения
# Вместо:
# <a href="/notes/create/">
# <a href="{% url 'note_create' %}">Создать заметку</a>