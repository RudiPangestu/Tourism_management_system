from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from destinations.models import Destination
from tours.models import Tour
from bookings.models import Booking
from reviews.models import TourReview, DestinationReview
from .serializers import (
    DestinationSerializer, TourSerializer, BookingSerializer,
    TourReviewSerializer, DestinationReviewSerializer
)


class IsOwnerOrStaff(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or staff to view/edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Staff can do anything
        if request.user.is_staff:
            return True
        
        # Check if object has a user field
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        return False


class DestinationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Destination.objects.filter(is_active=True)
    serializer_class = DestinationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['region', 'is_featured']
    search_fields = ['name', 'description', 'location']
    ordering_fields = ['name', 'created_at']
    
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        destination = self.get_object()
        reviews = destination.reviews.filter(is_approved=True)
        serializer = DestinationReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class TourViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tour.objects.filter(is_active=True)
    serializer_class = TourSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'difficulty', 'is_featured']
    search_fields = ['name', 'description', 'itinerary']
    ordering_fields = ['name', 'price', 'duration', 'created_at']
    
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        tour = self.get_object()
        reviews = tour.reviews.filter(is_approved=True)
        serializer = TourReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def dates(self, request, pk=None):
        from tours.models import TourDate
        from .serializers import TourDateSerializer
        from datetime import date
        
        tour = self.get_object()
        dates = tour.dates.filter(start_date__gte=date.today(), available_spots__gt=0).order_by('start_date')
        serializer = TourDateSerializer(dates, many=True)
        return Response(serializer.data)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['booking_date']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TourReviewViewSet(viewsets.ModelViewSet):
    queryset = TourReview.objects.filter(is_approved=True)
    serializer_class = TourReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrStaff]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['rating']
    ordering_fields = ['created_at', 'rating']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return TourReview.objects.all()
        if user.is_authenticated:
            return TourReview.objects.filter(is_approved=True) | TourReview.objects.filter(user=user)
        return TourReview.objects.filter(is_approved=True)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DestinationReviewViewSet(viewsets.ModelViewSet):
    queryset = DestinationReview.objects.filter(is_approved=True)
    serializer_class = DestinationReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrStaff]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['rating']
    ordering_fields = ['created_at', 'rating']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return DestinationReview.objects.all()
        if user.is_authenticated:
            return DestinationReview.objects.filter(is_approved=True) | DestinationReview.objects.filter(user=user)
        return DestinationReview.objects.filter(is_approved=True)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)