
from django.urls import path
from . import views

urlpatterns = [
    path('', views.tour_list, name='tour_list'),
    # Put all explicit paths BEFORE the slug pattern
    path('manage/', views.manage_tours, name='manage_tours'),
    path('create/', views.tour_create, name='tour_create'),
    path('dates/<int:tour_id>/', views.manage_tour_dates, name='manage_tour_dates'),
    # Put the catch-all slug patterns AFTER all explicit paths
    path('edit/<slug:slug>/', views.tour_edit, name='tour_edit'),
    path('delete/<slug:slug>/', views.tour_delete, name='tour_delete'),
    path('category/<int:category_id>/', views.category_tours, name='category_tours'),
    # This should be last as it will match any slug
    path('<slug:slug>/', views.tour_detail, name='tour_detail'),
]