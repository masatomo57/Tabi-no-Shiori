from tabinoshiori.models import Trip, Itinerary
from django.forms import ModelForm


class TripForm(ModelForm):
    class Meta:
        model = Trip
        fields = ['title', 'start_date', 'end_date', 'comment', 'is_public']

class ItineraryForm(ModelForm):
    class Meta:
        model = Itinerary
        fields = ['action', 'date', 'start_time', 'end_time']