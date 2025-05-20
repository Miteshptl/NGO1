from django.urls import path
from . import views

app_name = 'volunteers'

urlpatterns = [
    path('', views.volunteer_register, name='volunteer_register'),
    path('opportunities/', views.opportunity_list, name='opportunity_list'),
    path('opportunities/<int:pk>/', views.opportunity_detail, name='opportunity_detail'),
    path('apply/<int:pk>/', views.apply_opportunity, name='apply_opportunity'),
    path('profile/', views.volunteer_profile, name='volunteer_profile'),
    path('hours/', views.log_hours, name='log_hours'),
    path('hours/history/', views.hours_history, name='hours_history'),
] 