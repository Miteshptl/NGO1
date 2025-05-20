from django.urls import path
from . import views

app_name = 'donations'

urlpatterns = [
    path('donate/', views.donate, name='donate'),
    path('campaigns/', views.campaign_list, name='campaign_list'),
    path('campaigns/<int:pk>/', views.campaign_detail, name='campaign_detail'),
    path('recurring/', views.recurring_donation, name='recurring_donation'),
    path('history/', views.donation_history, name='donation_history'),
    path('success/', views.donation_success, name='donation_success'),
    path('cancel/', views.donation_cancel, name='donation_cancel'),
] 