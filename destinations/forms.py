from django import forms
from django.forms import inlineformset_factory
from .models import Destination, DestinationImage, Region, Attraction


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ['name', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = [
            'name', 'region', 'description', 'highlights', 'location',
            'latitude', 'longitude', 'featured_image', 'is_active', 'is_featured'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'highlights': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
        }


class DestinationImageForm(forms.ModelForm):
    class Meta:
        model = DestinationImage
        fields = ['image', 'caption', 'is_primary']


DestinationImageFormSet = inlineformset_factory(
    Destination, 
    DestinationImage, 
    form=DestinationImageForm,
    extra=3,
    can_delete=True
)


class AttractionForm(forms.ModelForm):
    class Meta:
        model = Attraction
        fields = ['name', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


AttractionFormSet = inlineformset_factory(
    Destination,
    Attraction,
    form=AttractionForm,
    extra=2,
    can_delete=True
)