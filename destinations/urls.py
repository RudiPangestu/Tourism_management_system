from django.urls import path
from . import views

urlpatterns = [
    path('', views.destination_list, name='destination_list'),
    path('<slug:slug>/', views.destination_detail, name='destination_detail'),
    path('region/<int:region_id>/', views.region_destinations, name='region_destinations'),
    path('manage/', views.manage_destinations, name='manage_destinations'),
    path('create/', views.destination_create, name='destination_create'),
    path('edit/<slug:slug>/', views.destination_edit, name='destination_edit'),
    path('delete/<slug:slug>/', views.destination_delete, name='destination_delete'),
]