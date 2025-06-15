from django import forms
from django.forms import inlineformset_factory
from .models import Booking, Participant, Payment


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['number_of_people', 'special_requests']
        widgets = {
            'special_requests': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['number_of_people'].widget.attrs.update({'min': 1, 'class': 'form-control'})


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'date_of_birth',
            'passport_number', 'nationality', 'emergency_contact',
            'emergency_phone', 'dietary_requirements', 'medical_conditions'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'dietary_requirements': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'medical_conditions': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }


ParticipantFormSet = inlineformset_factory(
    Booking,
    Participant,
    form=ParticipantForm,
    extra=1,
    can_delete=True
)


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method']