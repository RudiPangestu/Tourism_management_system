from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Tour, TourCategory, TourDate
from .forms import TourForm, TourDateForm, TourDateFormSet


def tour_list(request):
    tours = Tour.objects.filter(is_active=True)
    featured = Tour.objects.filter(is_featured=True, is_active=True)[:3]
    categories = TourCategory.objects.all()
    
    # Get filter parameters
    category_filter = request.GET.get('category')
    search_query = request.GET.get('search')
    
    # Apply category filter
    if category_filter:
        try:
            category_id = int(category_filter)
            tours = tours.filter(category_id=category_id)
        except (ValueError, TypeError):
            pass
    
    # Apply search filter
    if search_query:
        tours = tours.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    # Order tours
    tours = tours.order_by('-is_featured', 'name')
    
    return render(request, 'tours/tour_list.html', {
        'tours': tours,
        'featured': featured,
        'categories': categories,
        'selected_category': int(category_filter) if category_filter else None,
        'search_query': search_query,
    })


def tour_detail(request, slug):
    tour = get_object_or_404(Tour, slug=slug, is_active=True)
    dates = TourDate.objects.filter(tour=tour, available_spots__gt=0).order_by('start_date')
    related = Tour.objects.filter(category=tour.category).exclude(id=tour.id)[:3]
    
    return render(request, 'tours/tour_detail.html', {
        'tour': tour,
        'dates': dates,
        'related': related,
    })


def category_tours(request, category_id):
    category = get_object_or_404(TourCategory, id=category_id)
    tours = Tour.objects.filter(category=category, is_active=True)
    
    return render(request, 'tours/category_tours.html', {
        'category': category,
        'tours': tours,
    })


@login_required
def manage_tours(request):
    # Start with all tours
    tours = Tour.objects.all().select_related('category')
    
    # Get all categories for the filter dropdown
    categories = TourCategory.objects.all().order_by('name')
    
    # Apply filters
    category_filter = request.GET.get('category')
    status_filter = request.GET.get('status')
    featured_filter = request.GET.get('featured')
    search_query = request.GET.get('search')
    
    # Filter by category
    if category_filter:
        try:
            category_id = int(category_filter)
            tours = tours.filter(category_id=category_id)
        except (ValueError, TypeError):
            pass
    
    # Filter by status
    if status_filter == 'active':
        tours = tours.filter(is_active=True)
    elif status_filter == 'inactive':
        tours = tours.filter(is_active=False)
    
    # Filter by featured status
    if featured_filter == 'yes':
        tours = tours.filter(is_featured=True)
    elif featured_filter == 'no':
        tours = tours.filter(is_featured=False)
    
    # Filter by search query
    if search_query:
        tours = tours.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    # Order tours by featured status and then by name
    tours = tours.order_by('-is_featured', 'name')
    
    return render(request, 'tours/manage_tours.html', {
        'tours': tours,
        'categories': categories,
    })


@login_required
def tour_create(request):
    if request.method == 'POST':
        form = TourForm(request.POST, request.FILES)
        if form.is_valid():
            tour = form.save()
            messages.success(request, 'Tour created successfully!')
            return redirect('manage_tours')
    else:
        form = TourForm()
    
    return render(request, 'tours/tour_form.html', {
        'form': form,
        'title': 'Create Tour'
    })


@login_required
def tour_edit(request, slug):
    tour = get_object_or_404(Tour, slug=slug)
    
    if request.method == 'POST':
        form = TourForm(request.POST, request.FILES, instance=tour)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tour updated successfully!')
            return redirect('manage_tours')
    else:
        form = TourForm(instance=tour)
    
    return render(request, 'tours/tour_form.html', {
        'form': form,
        'tour': tour,
        'title': 'Edit Tour'
    })


@login_required
def tour_delete(request, slug):
    tour = get_object_or_404(Tour, slug=slug)
    
    if request.method == 'POST':
        tour.delete()
        messages.success(request, 'Tour deleted successfully!')
        return redirect('manage_tours')
    
    return render(request, 'tours/tour_confirm_delete.html', {
        'tour': tour,
    })


@login_required
def manage_tour_dates(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    
    if request.method == 'POST':
        formset = TourDateFormSet(request.POST, instance=tour)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Tour dates updated successfully!')
            return redirect('manage_tours')
    else:
        formset = TourDateFormSet(instance=tour)
    
    return render(request, 'tours/tour_dates_form.html', {
        'tour': tour,
        'formset': formset,
    })