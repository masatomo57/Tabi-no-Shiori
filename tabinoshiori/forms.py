from typing import Any, Dict, Mapping, Optional, Type, Union
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from tabinoshiori.models import Trip, Itinerary
from django.forms import ModelForm, DateInput, TimeInput, TextInput
from django import forms


class TripForm(ModelForm):
    class Meta:
        model = Trip
        fields = ['title', 'start_date', 'end_date', 'comment', 'is_public']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        } # inputのtypeを設定


class ItineraryForm(ModelForm):
    class Meta:
        model = Itinerary
        fields = ['action', 'date', 'start_time', 'end_time']
        widgets = {
            'date': DateInput(attrs={'required': True, 'type': 'date'}),
            'start_time': TimeInput(attrs={'required': True, 'type': 'time'}),
            'end_time': TimeInput(attrs={'required': True, 'type': 'time'}),
            'action': TextInput(attrs={'required': True})
        }
        labels = {
            'action': '',
            'date': '',
            'start_time': '',
            'end_time': '',
        }