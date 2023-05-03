from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from tabinoshiori.models import Trip, Itinerary
from tabinoshiori.forms import TripForm, ItineraryForm
from django.urls import reverse, reverse_lazy


# Create your views here.
class MyHome(LoginRequiredMixin, TemplateView):
    template_name = 'tabinoshiori/home.html'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['trips'] = Trip.objects.filter(username__username=context['user'].username)
        return context

class MyRegisterTrip(LoginRequiredMixin, CreateView):
    model = Trip
    form_class = TripForm
    template_name = 'tabinoshiori/register.html'
    success_url = reverse_lazy('tabinoshiori:home')
    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)


