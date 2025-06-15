
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from destinations.models import Destination


class TourCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Tour Categories"
    
    def __str__(self):
        return self.name


class Tour(models.Model):
    DIFFICULTY_CHOICES = (
        ('easy', 'Easy'),
        ('moderate', 'Moderate'),
        ('challenging', 'Challenging'),
        ('difficult', 'Difficult'),
    )
    
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    category = models.ForeignKey(TourCategory, on_delete=models.CASCADE, related_name='tours')
    destinations = models.ManyToManyField(Destination, related_name='tours')
    description = models.TextField()
    itinerary = models.TextField()
    duration = models.PositiveIntegerField(help_text="Duration in days")
    group_size = models.PositiveIntegerField(help_text="Maximum group size")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    included = models.TextField(help_text="What's included in the tour")
    not_included = models.TextField(help_text="What's not included in the tour")
    featured_image = models.ImageField(upload_to='tours/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-is_featured', 'name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('tour_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class TourDate(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='dates')
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price for this specific date")
    available_spots = models.PositiveIntegerField()
    is_guaranteed = models.BooleanField(default=False, help_text="Whether the departure is guaranteed")
    
    class Meta:
        ordering = ['start_date']
    
    def __str__(self):
        return f"{self.tour.name} - {self.start_date}"