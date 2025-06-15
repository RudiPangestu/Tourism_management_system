from django.contrib import admin
from .models import TourCategory, Tour, TourDate


class TourDateInline(admin.TabularInline):
    model = TourDate
    extra = 3


@admin.register(TourCategory)
class TourCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'duration', 'price', 'is_active', 'is_featured')
    list_filter = ('category', 'difficulty', 'is_active', 'is_featured')
    search_fields = ('name', 'description', 'itinerary')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [TourDateInline]
    list_editable = ('is_active', 'is_featured')
    filter_horizontal = ('destinations',)