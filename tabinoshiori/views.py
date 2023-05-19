from typing import Any, Dict
from django.forms.models import BaseModelForm, modelformset_factory
from django.http import HttpResponse
from django.views.generic import TemplateView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from tabinoshiori.models import Trip, Itinerary
from tabinoshiori.forms import TripForm, ItineraryForm
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import login_required


# Create your views here.
class MyHome(LoginRequiredMixin, TemplateView):
    template_name = 'tabinoshiori/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['trips'] = Trip.objects.filter(username__username=context['user'].username)
        return context

class MyItineraryView(LoginRequiredMixin, DetailView):
    model = Trip
    template_name = 'tabinoshiori/trip.html'
    '''
    def get_object(self, queryset=None):
        object = dict()        
        if queryset is None:
            queryset = self.get_queryset()
            
        queryset = queryset.filter(username__username=self.request.user.username)
        object['itinerarys'] = super().get_object(queryset=queryset)
        return object
    '''
    
class MyRegisterTrip(LoginRequiredMixin, CreateView):
    model = Trip
    form_class = TripForm
    template_name = 'tabinoshiori/registertrip.html'
    success_url = reverse_lazy('tabinoshiori:home')
    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

@login_required
def MyRegisterItinerary(request):
    template_name = 'tabinoshiori/registeritinerary.html'
    
    # フォームセット定義
    MyFormSet = modelformset_factory(
        model=Itinerary,
        form=ItineraryForm,
        extra=3
        max_num=3
    )
    
    if request.method=='POST':
        return 
    else:
        return
    

'''
class MyRegisterItinerary(LoginRequiredMixin, CreateView):
    model = Itinerary
    form_class = ItineraryForm
    template_name = 'tabinoshiori/registeritinerary.html'
    def form_valid(self, form):
        form.instance.username = self.request.user
        form.instance.title = get_object_or_404(Trip, pk=self.kwargs.get('pk'))
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = get_object_or_404(Trip, pk=self.kwargs.get('pk'))
        return context
    def get_success_url(self):
        return reverse('tabinoshiori:itinerary', kwargs={'pk': self.kwargs.get('pk')})
'''