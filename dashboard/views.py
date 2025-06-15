from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Avg, Sum
from django.db.models.functions import TruncMonth
from django.contrib.auth.models import User
from tours.models import Tour, TourDate
from destinations.models import Destination
from bookings.models import Booking
from reviews.models import TourReview, DestinationReview
from django.http import JsonResponse
import datetime
import json


def is_staff(user):
    return user.is_staff


@login_required
@user_passes_test(is_staff)
def dashboard(request):
    # Get some statistics for the dashboard
    total_tours = Tour.objects.count()
    total_destinations = Destination.objects.count()
    total_bookings = Booking.objects.count()
    total_users = User.objects.count()
    recent_bookings = Booking.objects.order_by('-booking_date')[:5]
    
    # Total revenue
    total_revenue = Booking.objects.filter(status='confirmed').aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    # Average ratings
    avg_tour_rating = TourReview.objects.filter(is_approved=True).aggregate(Avg('rating'))['rating__avg'] or 0
    avg_destination_rating = DestinationReview.objects.filter(is_approved=True).aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Upcoming tour dates
    from datetime import date
    upcoming_tours = TourDate.objects.filter(start_date__gte=date.today()).order_by('start_date')[:5]
    
    # Get popular destinations for sidebar
    popular_destinations = Destination.objects.annotate(
        booking_count=Count('tours__bookings', distinct=True)
    ).filter(booking_count__gt=0).order_by('-booking_count')[:5]
    
    # Revenue by month for the current year
    current_year = datetime.datetime.now().year
    revenue_by_month = Booking.objects.filter(
        booking_date__year=current_year, 
        status='confirmed'
    ).annotate(
        month=TruncMonth('booking_date')
    ).values(
        'month'
    ).annotate(
        total=Sum('total_price')
    ).order_by('month')
    
    # Prepare revenue data for chart
    revenue_data = {}
    for item in revenue_by_month:
        month_num = item['month'].month
        revenue_data[month_num] = float(item['total']) if item['total'] else 0
    
    # Fill missing months with 0
    monthly_revenue = []
    for month in range(1, 13):
        monthly_revenue.append(revenue_data.get(month, 0))
    
    return render(request, 'dashboard/dashboard.html', {
        'total_tours': total_tours,
        'total_destinations': total_destinations,
        'total_bookings': total_bookings,
        'total_users': total_users,
        'recent_bookings': recent_bookings,
        'total_revenue': total_revenue,
        'avg_tour_rating': avg_tour_rating,
        'avg_destination_rating': avg_destination_rating,
        'upcoming_tours': upcoming_tours,
        'popular_destinations': popular_destinations,
        'monthly_revenue': json.dumps(monthly_revenue),  # Convert to JSON for JavaScript
    })


@login_required
@user_passes_test(is_staff)
def revenue_data_api(request):
    """API endpoint to get revenue data for charts"""
    current_year = datetime.datetime.now().year
    
    # Get revenue by month
    revenue_by_month = Booking.objects.filter(
        booking_date__year=current_year, 
        status='confirmed'
    ).annotate(
        month=TruncMonth('booking_date')
    ).values(
        'month'
    ).annotate(
        total=Sum('total_price')
    ).order_by('month')
    
    # Prepare data
    revenue_data = {}
    for item in revenue_by_month:
        month_num = item['month'].month
        revenue_data[month_num] = float(item['total']) if item['total'] else 0
    
    # Fill missing months with 0
    monthly_revenue = []
    month_labels = []
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    for month in range(1, 13):
        monthly_revenue.append(revenue_data.get(month, 0))
        month_labels.append(months[month-1])
    
    return JsonResponse({
        'labels': month_labels,
        'data': monthly_revenue,
        'year': current_year
    })


@login_required
@user_passes_test(is_staff)
def booking_stats(request):
    # Bookings by status
    booking_by_status = Booking.objects.values('status').annotate(count=Count('id')).order_by('status')
    
    # Bookings by month (for the current year)
    current_year = datetime.datetime.now().year
    booking_by_month = Booking.objects.filter(booking_date__year=current_year) \
        .annotate(month=TruncMonth('booking_date')) \
        .values('month') \
        .annotate(count=Count('id')) \
        .order_by('month')
    
    # Revenue by month
    revenue_by_month = Booking.objects.filter(
        booking_date__year=current_year, 
        status='confirmed'
    ).annotate(
        month=TruncMonth('booking_date')
    ).values(
        'month'
    ).annotate(
        total=Sum('total_price')
    ).order_by('month')
    
    return render(request, 'dashboard/booking_stats.html', {
        'booking_by_status': booking_by_status,
        'booking_by_month': booking_by_month,
        'revenue_by_month': revenue_by_month,
    })


@login_required
@user_passes_test(is_staff)
def destination_stats(request):
    # Most popular destinations (by number of bookings)
    popular_destinations = Destination.objects.annotate(
        booking_count=Count('tours__bookings', distinct=True)
    ).order_by('-booking_count')[:10]
    
    # Destinations by region
    destinations_by_region = Destination.objects.values('region__name').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Highest rated destinations
    highest_rated = Destination.objects.annotate(
        avg_rating=Avg('reviews__rating')
    ).filter(
        avg_rating__isnull=False
    ).order_by('-avg_rating')[:10]
    
    return render(request, 'dashboard/destination_stats.html', {
        'popular_destinations': popular_destinations,
        'destinations_by_region': destinations_by_region,
        'highest_rated': highest_rated,
    })


@login_required
@user_passes_test(is_staff)
def tour_stats(request):
    # Most booked tours
    popular_tours = Tour.objects.annotate(
        booking_count=Count('bookings')
    ).order_by('-booking_count')[:10]
    
    # Tours by category
    tours_by_category = Tour.objects.values('category__name').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Tours by difficulty
    tours_by_difficulty = Tour.objects.values('difficulty').annotate(
        count=Count('id')
    ).order_by('difficulty')
    
    # Highest rated tours
    highest_rated = Tour.objects.annotate(
        avg_rating=Avg('reviews__rating')
    ).filter(
        avg_rating__isnull=False
    ).order_by('-avg_rating')[:10]
    
    return render(request, 'dashboard/tour_stats.html', {
        'popular_tours': popular_tours,
        'tours_by_category': tours_by_category,
        'tours_by_difficulty': tours_by_difficulty,
        'highest_rated': highest_rated,
    })


@login_required
@user_passes_test(is_staff)
def review_stats(request):
    # Review distribution by rating (tour)
    tour_ratings = TourReview.objects.values('rating').annotate(
        count=Count('id')
    ).order_by('rating')
    
    # Review distribution by rating (destination)
    destination_ratings = DestinationReview.objects.values('rating').annotate(
        count=Count('id')
    ).order_by('rating')
    
    # Recent reviews
    recent_tour_reviews = TourReview.objects.order_by('-created_at')[:10]
    recent_destination_reviews = DestinationReview.objects.order_by('-created_at')[:10]
    
    # Reviews needing approval
    pending_reviews_count = TourReview.objects.filter(is_approved=False).count() + \
                         DestinationReview.objects.filter(is_approved=False).count()
    
    return render(request, 'dashboard/review_stats.html', {
        'tour_ratings': tour_ratings,
        'destination_ratings': destination_ratings,
        'recent_tour_reviews': recent_tour_reviews,
        'recent_destination_reviews': recent_destination_reviews,
        'pending_reviews_count': pending_reviews_count,
    })


@login_required
@user_passes_test(is_staff)
def user_stats(request):
    # User registration by month
    user_registrations = User.objects.annotate(
        month=TruncMonth('date_joined')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    # Most active users (by number of bookings)
    active_users = User.objects.annotate(
        booking_count=Count('bookings')
    ).order_by('-booking_count')[:10]
    
    # Most active reviewers
    active_reviewers = User.objects.annotate(
        review_count=Count('reviews')
    ).order_by('-review_count')[:10]
    
    return render(request, 'dashboard/user_stats.html', {
        'user_registrations': user_registrations,
        'active_users': active_users,
        'active_reviewers': active_reviewers,
    })