from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking_list, name='booking_list'),
    path('<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('create/<int:tour_date_id>/', views.booking_create, name='booking_create'),
    path('manage/', views.manage_bookings, name='manage_bookings'),
    path('edit/<int:booking_id>/', views.booking_edit, name='booking_edit'),
    path('cancel/<int:booking_id>/', views.booking_cancel, name='booking_cancel'),
    path('confirm/<int:booking_id>/', views.booking_confirm, name='booking_confirm'),
    path('receipt/<int:booking_id>/', views.booking_receipt, name='booking_receipt'),
]