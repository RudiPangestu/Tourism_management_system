from django import forms
from django.forms import inlineformset_factory
from .models import TourReview, DestinationReview, ReviewImage


class TourReviewForm(forms.ModelForm):
    class Meta:
        model = TourReview
        fields = ['title', 'content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
        }


class DestinationReviewForm(forms.ModelForm):
    class Meta:
        model = DestinationReview
        fields = ['title', 'content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
        }


class ReviewImageForm(forms.ModelForm):
    class Meta:
        model = ReviewImage
        fields = ['image', 'caption']


ReviewImageFormSet = inlineformset_factory(
    TourReview,
    ReviewImage,
    form=ReviewImageForm,
    extra=3,
    can_delete=True
)

DestinationReviewImageFormSet = inlineformset_factory(
    DestinationReview,
    ReviewImage,
    form=ReviewImageForm,
    extra=3,
    can_delete=True
)