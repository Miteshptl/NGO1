from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('<slug:slug>/', views.event_detail, name='event_detail'),
    path('register/<slug:slug>/', views.event_register, name='event_register'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<slug:slug>/', views.category_detail, name='category_detail'),
    path('speakers/', views.speaker_list, name='speaker_list'),
    path('speakers/<int:pk>/', views.speaker_detail, name='speaker_detail'),
    path('calendar/', views.event_calendar, name='event_calendar'),
] 