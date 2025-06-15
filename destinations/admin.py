from django.contrib import admin
from .models import Region, Destination, DestinationImage, Attraction


class DestinationImageInline(admin.TabularInline):
    model = DestinationImage
    extra = 3


class AttractionInline(admin.TabularInline):
    model = Attraction
    extra = 2


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'location', 'is_active', 'is_featured', 'created_at')
    list_filter = ('region', 'is_active', 'is_featured')
    search_fields = ('name', 'description', 'location')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [DestinationImageInline, AttractionInline]
    list_editable = ('is_active', 'is_featured')
    date_hierarchy = 'created_at'