from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Destination, Region
from .forms import DestinationForm, DestinationImageFormSet

def destination_list(request):
    # Start with all active destinations
    destinations = Destination.objects.filter(is_active=True)
    regions = Region.objects.all().order_by('name')
    
    # Get filter parameters
    region_filter = request.GET.get('region')
    search_query = request.GET.get('search')
    
    # Apply region filter
    selected_region = ""
    if region_filter:
        try:
            region_id = int(region_filter)
            destinations = destinations.filter(region_id=region_id)
            selected_region = region_id
        except (ValueError, TypeError):
            pass
    
    # Apply search filter
    if search_query:
        destinations = destinations.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(highlights__icontains=search_query) |
            Q(region__name__icontains=search_query)
        )
    
    # After applying all filters, separate featured and non-featured destinations
    featured = destinations.filter(is_featured=True)[:3]
    all_destinations = destinations.order_by('-is_featured', 'name')
    
    return render(request, 'destinations/destination_list.html', {
        'destinations': all_destinations,
        'featured': featured,
        'regions': regions,
        'selected_region': selected_region,
        'search_query': search_query,
    })


def destination_detail(request, slug):
    destination = get_object_or_404(Destination, slug=slug, is_active=True)
    related = Destination.objects.filter(region=destination.region).exclude(id=destination.id)[:3]
    
    return render(request, 'destinations/destination_detail.html', {
        'destination': destination,
        'related': related,
    })


def region_destinations(request, region_id):
    region = get_object_or_404(Region, id=region_id)
    destinations = Destination.objects.filter(region=region, is_active=True)
    
    return render(request, 'destinations/region_destinations.html', {
        'region': region,
        'destinations': destinations,
    })


@login_required
def manage_destinations(request):
    # Start with all destinations
    destinations = Destination.objects.all().select_related('region')
    
    # Get all regions for the filter dropdown
    regions = Region.objects.all().order_by('name')
    
    # Apply filters
    region_filter = request.GET.get('region')
    status_filter = request.GET.get('status')
    featured_filter = request.GET.get('featured')
    search_query = request.GET.get('search')
    
    # Filter by region
    if region_filter:
        try:
            region_id = int(region_filter)
            destinations = destinations.filter(region_id=region_id)
        except (ValueError, TypeError):
            pass
    
    # Filter by status
    if status_filter == 'active':
        destinations = destinations.filter(is_active=True)
    elif status_filter == 'inactive':
        destinations = destinations.filter(is_active=False)
    
    # Filter by featured status
    if featured_filter == 'yes':
        destinations = destinations.filter(is_featured=True)
    elif featured_filter == 'no':
        destinations = destinations.filter(is_featured=False)
    
    # Filter by search query
    if search_query:
        destinations = destinations.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(region__name__icontains=search_query)
        )
    
    # Order destinations by featured status and then by name
    destinations = destinations.order_by('-is_featured', 'name')
    
    return render(request, 'destinations/manage_destinations.html', {
        'destinations': destinations,
        'regions': regions,
    })


@login_required
def destination_create(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES)
        formset = DestinationImageFormSet(request.POST, request.FILES, instance=Destination())
        
        if form.is_valid() and formset.is_valid():
            destination = form.save()
            formset.instance = destination
            formset.save()
            messages.success(request, 'Destination created successfully!')
            return redirect('manage_destinations')
    else:
        form = DestinationForm()
        formset = DestinationImageFormSet(instance=Destination())
    
    return render(request, 'destinations/destination_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Create Destination'
    })


@login_required
def destination_edit(request, slug):
    destination = get_object_or_404(Destination, slug=slug)
    
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES, instance=destination)
        formset = DestinationImageFormSet(request.POST, request.FILES, instance=destination)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Destination updated successfully!')
            return redirect('manage_destinations')
    else:
        form = DestinationForm(instance=destination)
        formset = DestinationImageFormSet(instance=destination)
    
    return render(request, 'destinations/destination_form.html', {
        'form': form,
        'formset': formset,
        'destination': destination,
        'title': 'Edit Destination'
    })


@login_required
def destination_delete(request, slug):
    destination = get_object_or_404(Destination, slug=slug)
    
    if request.method == 'POST':
        destination.delete()
        messages.success(request, 'Destination deleted successfully!')
        return redirect('manage_destinations')
    
    return render(request, 'destinations/destination_confirm_delete.html', {
        'destination': destination,
    })