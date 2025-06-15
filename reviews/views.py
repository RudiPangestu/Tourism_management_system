from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TourReview, DestinationReview, ReviewImage
from tours.models import Tour
from destinations.models import Destination
from .forms import TourReviewForm, DestinationReviewForm, ReviewImageFormSet


def tour_reviews(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    reviews = TourReview.objects.filter(tour=tour, is_approved=True)
    
    return render(request, 'reviews/tour_reviews.html', {
        'tour': tour,
        'reviews': reviews,
    })


def destination_reviews(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)
    reviews = DestinationReview.objects.filter(destination=destination, is_approved=True)
    
    return render(request, 'reviews/destination_reviews.html', {
        'destination': destination,
        'reviews': reviews,
    })


@login_required
def create_tour_review(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    
    # Check if user has already reviewed this tour
    if TourReview.objects.filter(user=request.user, tour=tour).exists():
        messages.error(request, 'You have already reviewed this tour.')
        return redirect('tour_reviews', tour_id=tour.id)
    
    if request.method == 'POST':
        form = TourReviewForm(request.POST)
        formset = ReviewImageFormSet(request.POST, request.FILES)
        
        if form.is_valid() and formset.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.tour = tour
            review.save()
            
            images = formset.save(commit=False)
            for image in images:
                image.tour_review = review
                image.save()
            
            messages.success(request, 'Your review has been submitted')
            return redirect('tour_reviews', tour_id=tour.id)
    else:
        form = TourReviewForm()
        formset = ReviewImageFormSet()
    
    return render(request, 'reviews/create_tour_review.html', {
        'form': form,
        'formset': formset,
        'tour': tour,
    })


@login_required
def create_destination_review(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)
    
    # Check if user has already reviewed this destination
    if DestinationReview.objects.filter(user=request.user, destination=destination).exists():
        messages.error(request, 'You have already reviewed this destination.')
        return redirect('destination_reviews', destination_id=destination.id)
    
    if request.method == 'POST':
        form = DestinationReviewForm(request.POST)
        formset = ReviewImageFormSet(request.POST, request.FILES)
        
        if form.is_valid() and formset.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.destination = destination
            review.save()
            
            images = formset.save(commit=False)
            for image in images:
                image.destination_review = review
                image.save()
            
            messages.success(request, 'Your review has been submitted')
            return redirect('destination_reviews', destination_id=destination.id)
    else:
        form = DestinationReviewForm()
        formset = ReviewImageFormSet()
    
    return render(request, 'reviews/create_destination_review.html', {
        'form': form,
        'formset': formset,
        'destination': destination,
    })


@login_required
def edit_tour_review(request, review_id):
    review = get_object_or_404(TourReview, id=review_id, user=request.user)
    
    if request.method == 'POST':
        form = TourReviewForm(request.POST, instance=review)
        formset = ReviewImageFormSet(request.POST, request.FILES, instance=review)
        
        if form.is_valid() and formset.is_valid():
            review = form.save(commit=False)
            review.is_approved = False  # Reset approval status
            review.save()
            formset.save()
            
            messages.success(request, 'Your review has been updated and.')
            return redirect('tour_reviews', tour_id=review.tour.id)
    else:
        form = TourReviewForm(instance=review)
        formset = ReviewImageFormSet(instance=review)
    
    return render(request, 'reviews/edit_tour_review.html', {
        'form': form,
        'formset': formset,
        'review': review,
    })


@login_required
def edit_destination_review(request, review_id):
    review = get_object_or_404(DestinationReview, id=review_id, user=request.user)
    
    if request.method == 'POST':
        form = DestinationReviewForm(request.POST, instance=review)
        formset = ReviewImageFormSet(request.POST, request.FILES, instance=review)
        
        if form.is_valid() and formset.is_valid():
            review = form.save(commit=False)
            review.is_approved = False  # Reset approval status
            review.save()
            formset.save()
            
            messages.success(request, 'Your review has been updated.')
            return redirect('destination_reviews', destination_id=review.destination.id)
    else:
        form = DestinationReviewForm(instance=review)
        formset = ReviewImageFormSet(instance=review)
    
    return render(request, 'reviews/edit_destination_review.html', {
        'form': form,
        'formset': formset,
        'review': review,
    })


@login_required
def manage_reviews(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    tour_reviews = TourReview.objects.all().order_by('-created_at')
    destination_reviews = DestinationReview.objects.all().order_by('-created_at')
    
    if request.method == 'POST':
        review_type = request.POST.get('review_type')
        review_id = request.POST.get('review_id')
        action = request.POST.get('action')
        
        if review_type == 'tour':
            review = get_object_or_404(TourReview, id=review_id)
        else:
            review = get_object_or_404(DestinationReview, id=review_id)
        
        if action == 'approve':
            review.is_approved = True
            review.save()
            messages.success(request, 'Review approved successfully.')
        elif action == 'reject':
            review.is_approved = False
            review.save()
            messages.success(request, 'Review rejected successfully.')
        elif action == 'delete':
            review.delete()
            messages.success(request, 'Review deleted successfully.')
        
        return redirect('manage_reviews')
    
    return render(request, 'reviews/manage_reviews.html', {
        'tour_reviews': tour_reviews,
        'destination_reviews': destination_reviews,
    })