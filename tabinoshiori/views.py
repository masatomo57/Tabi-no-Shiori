from typing import Any, Dict
from django.forms import formset_factory
from django.forms.models import BaseModelForm, modelformset_factory, inlineformset_factory
from django.http import HttpResponse
from django.views.generic import TemplateView, CreateView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from tabinoshiori.models import Trip, Itinerary
from tabinoshiori.forms import TripForm, ItineraryForm
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def HomeView(request):
    user = request.user
    context = {
        "user": user,
        "trips": Trip.objects.filter(username__username=user.username).order_by('start_date'),
    }
    return render(request, 'tabinoshiori/home.html', context)

'''
class MyHome(LoginRequiredMixin, TemplateView):
    template_name = 'tabinoshiori/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['trips'] = Trip.objects.filter(username__username=context['user'].username)
        return context
'''

@login_required
def ItineraryView(request, pk):
    user = request.user
    trip = Trip.objects.get(username__username=user.username, id=pk)
    context = {
        "title": trip.title,
        "id": trip.id,
        "itinerarys": Itinerary.objects.filter(username__username=user.username, title__title=trip.title).order_by('date', 'start_time'),
    }
    return render(request, 'tabinoshiori/trip.html', context)


'''
class ItineraryView(LoginRequiredMixin, DetailView):
    model = Trip
    template_name = 'tabinoshiori/trip.html'
'''
    
class RegisterTripView(LoginRequiredMixin, CreateView):
    model = Trip
    form_class = TripForm
    template_name = 'tabinoshiori/registertrip.html'
    success_url = reverse_lazy('tabinoshiori:home')
    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

'''
class MyRegisterItinerary(FormView, LoginRequiredMixin):
    template_name="tabinoshiori/registeritinerary.html"
    ItineraryFormSet = formset_factory(
        model=Itinerary,
        form=ItineraryForm,
        extra=1,
    )
    form_class = ItineraryFormSet
    
    def get_success_url(self):
        return reverse('tabinoshiori:itinerary', kwargs={'pk': self.kwargs.get('pk')})
'''


@login_required
def RegisterItineraryView(request, pk):
    
    # フォームセット定義
    MyFormSet = modelformset_factory(
        model=Itinerary,
        form=ItineraryForm,
        extra=2,
        max_num=30,
    )
    
    if request.method=='POST':
        form_set = MyFormSet(request.POST)
        if form_set.is_valid():
            with transaction.atomic():
                for form in form_set:
                    itinerary = form.save(commit=False)
                    itinerary.title = get_object_or_404(Trip, pk=pk)
                    itinerary.username = request.user
                    itinerary.save()
            return redirect('tabinoshiori:itinerary', pk=pk)
        
        else:
            context = {
                "form_set": form_set,
                "title": get_object_or_404(Trip, pk=pk),
                "message": form_set.non_form_errors,
            }
            return render(request, "tabinoshiori/registeritinerary.html", context)
        
    elif request.method=='GET':
        form_set = MyFormSet(queryset=Itinerary.objects.none())
        context = {
            "form_set": form_set,
            "title": get_object_or_404(Trip, pk=pk),
        }
        
        return render(request, "tabinoshiori/registeritinerary.html", context)



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