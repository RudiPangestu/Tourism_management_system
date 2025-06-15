from django.contrib import admin
from .models import TourReview, DestinationReview, ReviewImage


class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 1


@admin.register(TourReview)
class TourReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'tour', 'user', 'rating', 'created_at', 'is_approved')
    list_filter = ('rating', 'is_approved', 'created_at')
    search_fields = ('user__username', 'title', 'content', 'tour__name')
    list_editable = ('is_approved',)
    date_hierarchy = 'created_at'
    inlines = [ReviewImageInline]


@admin.register(DestinationReview)
class DestinationReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'destination', 'user', 'rating', 'created_at', 'is_approved')
    list_filter = ('rating', 'is_approved', 'created_at')
    search_fields = ('user__username', 'title', 'content', 'destination__name')
    list_editable = ('is_approved',)
    date_hierarchy = 'created_at'
    inlines = [ReviewImageInline]