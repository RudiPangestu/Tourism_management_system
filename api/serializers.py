from rest_framework import serializers
from destinations.models import Destination, Region, Attraction
from tours.models import Tour, TourCategory, TourDate
from bookings.models import Booking, Participant
from reviews.models import TourReview, DestinationReview


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name', 'description', 'image']


class AttractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attraction
        fields = ['id', 'name', 'description', 'image']


class DestinationSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    attractions = AttractionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Destination
        fields = [
            'id', 'name', 'slug', 'region', 'description', 'highlights',
            'location', 'latitude', 'longitude', 'featured_image',
            'attractions', 'is_active', 'is_featured'
        ]


class TourCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TourCategory
        fields = ['id', 'name', 'description']


class TourDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourDate
        fields = ['id', 'start_date', 'end_date', 'price', 'available_spots', 'is_guaranteed']


class TourSerializer(serializers.ModelSerializer):
    category = TourCategorySerializer(read_only=True)
    destinations = DestinationSerializer(many=True, read_only=True)
    dates = TourDateSerializer(many=True, read_only=True)
    
    class Meta:
        model = Tour
        fields = [
            'id', 'name', 'slug', 'category', 'destinations', 'description',
            'itinerary', 'duration', 'group_size', 'difficulty', 'price',
            'discount_price', 'included', 'not_included', 'featured_image',
            'dates', 'is_active', 'is_featured'
        ]


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone',
            'date_of_birth', 'passport_number', 'nationality',
            'emergency_contact', 'emergency_phone', 'dietary_requirements',
            'medical_conditions'
        ]


class BookingSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True, read_only=True)
    tour = TourSerializer(read_only=True)
    tour_date = TourDateSerializer(read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'tour', 'tour_date', 'booking_date',
            'number_of_people', 'total_price', 'status',
            'special_requests', 'confirmation_code', 'participants'
        ]
        read_only_fields = ['user', 'booking_date', 'confirmation_code']


class TourReviewSerializer(serializers.ModelSerializer):
    tour = TourSerializer(read_only=True)
    
    class Meta:
        model = TourReview
        fields = ['id', 'user', 'tour', 'title', 'content', 'rating', 'created_at', 'is_approved']
        read_only_fields = ['user', 'created_at', 'is_approved']


class DestinationReviewSerializer(serializers.ModelSerializer):
    destination = DestinationSerializer(read_only=True)
    
    class Meta:
        model = DestinationReview
        fields = ['id', 'user', 'destination', 'title', 'content', 'rating', 'created_at', 'is_approved']
        read_only_fields = ['user', 'created_at', 'is_approved']