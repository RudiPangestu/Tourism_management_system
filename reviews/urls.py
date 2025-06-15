from django.urls import path
from . import views

urlpatterns = [
    path('tour/<int:tour_id>/', views.tour_reviews, name='tour_reviews'),
    path('destination/<int:destination_id>/', views.destination_reviews, name='destination_reviews'),
    path('tour/create/<int:tour_id>/', views.create_tour_review, name='create_tour_review'),
    path('destination/create/<int:destination_id>/', views.create_destination_review, name='create_destination_review'),
    path('tour/edit/<int:review_id>/', views.edit_tour_review, name='edit_tour_review'),
    path('destination/edit/<int:review_id>/', views.edit_destination_review, name='edit_destination_review'),
    path('manage/', views.manage_reviews, name='manage_reviews'),
]