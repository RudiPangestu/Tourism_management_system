from django import forms
from django.forms import inlineformset_factory
from .models import Tour, TourDate, TourCategory


class TourCategoryForm(forms.ModelForm):
    class Meta:
        model = TourCategory
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = [
            'name', 'category', 'destinations', 'description', 'itinerary',
            'duration', 'group_size', 'difficulty', 'price', 'discount_price',
            'included', 'not_included', 'featured_image', 'is_active', 'is_featured'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'itinerary': forms.Textarea(attrs={'rows': 10, 'class': 'form-control'}),
            'included': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'not_included': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'destinations': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
        }


class TourDateForm(forms.ModelForm):
    class Meta:
        model = TourDate
        fields = ['start_date', 'end_date', 'price', 'available_spots', 'is_guaranteed']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


TourDateFormSet = inlineformset_factory(
    Tour,
    TourDate,
    form=TourDateForm,
    extra=3,
    can_delete=True
)