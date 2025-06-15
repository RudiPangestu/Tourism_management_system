from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/revenue-data/', views.revenue_data_api, name='revenue_data_api'),
    path('bookings/', views.booking_stats, name='booking_stats'),
    path('destinations/', views.destination_stats, name='destination_stats'),
    path('tours/', views.tour_stats, name='tour_stats'),
    path('reviews/', views.review_stats, name='review_stats'),
    path('users/', views.user_stats, name='user_stats'),
]