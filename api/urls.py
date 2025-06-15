from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'destinations', views.DestinationViewSet)
router.register(r'tours', views.TourViewSet)
router.register(r'bookings', views.BookingViewSet)
router.register(r'tourreviews', views.TourReviewViewSet)
router.register(r'destinationreviews', views.DestinationReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]