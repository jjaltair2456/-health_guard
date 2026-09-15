from django.urls import path
from .views import profile_view

app_name = 'users'

urlpatterns = [
    path('perfil/', profile_view, name='profile'),
]