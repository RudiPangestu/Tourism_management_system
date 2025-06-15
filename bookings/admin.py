from django.contrib import admin
from .models import Booking, Participant, Payment


class ParticipantInline(admin.TabularInline):
    model = Participant
    extra = 0


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tour', 'booking_date', 'number_of_people', 'total_price', 'status')
    list_filter = ('status', 'booking_date')
    search_fields = ('user__username', 'user__email', 'tour__name', 'confirmation_code')
    date_hierarchy = 'booking_date'
    inlines = [ParticipantInline, PaymentInline]
    readonly_fields = ('confirmation_code',)