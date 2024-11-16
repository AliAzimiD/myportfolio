from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.profile_view, name='profile'),
    path('update/', views.profile_update, name='profile_update'),
]