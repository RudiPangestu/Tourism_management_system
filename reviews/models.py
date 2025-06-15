from django.db import models
from django.contrib.auth.models import User
from tours.models import Tour
from destinations.models import Destination


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1 - Poor'),
        (2, '2 - Below Average'),
        (3, '3 - Average'),
        (4, '4 - Good'),
        (5, '5 - Excellent'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)
    
    class Meta:
        abstract = True
        ordering = ['-created_at']


class TourReview(Review):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tour_reviews')

    def __str__(self):
        return f"Review for {self.tour.name} by {self.user.username}"


class DestinationReview(Review):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='destination_reviews')

    def __str__(self):
        return f"Review for {self.destination.name} by {self.user.username}"


class ReviewImage(models.Model):
    tour_review = models.ForeignKey(TourReview, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    destination_review = models.ForeignKey(DestinationReview, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    image = models.ImageField(upload_to='reviews/')
    caption = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        if self.tour_review:
            return f"Image for {self.tour_review}"
        return f"Image for {self.destination_review}"