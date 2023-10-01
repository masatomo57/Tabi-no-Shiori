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

from datetime import timedelta

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
    start_date = trip.start_date
    end_date = trip.end_date
    
    # itinerarys = Itinerary.objects.filter(username__username=user.username, title__title=trip.title).order_by('date', 'start_time')
    itinerarys_list = []
    dates = Itinerary.objects.filter(username__username=user.username, title__title=trip.title).order_by("date").distinct().values_list("date", flat=True)
    for date in dates:
        itinerarys_list.append(Itinerary.objects.filter(username__username=user.username, title__title=trip.title, date=date).order_by("start_time"))
    
    '''
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)
    '''
    context = {
        "title": trip.title,
        "id": trip.id,
        "itinerarys_list": itinerarys_list,
        "dates": dates,
        "start_date": start_date,
        "end_date": end_date,
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
    # 必要な変数の定義
    user = request.user
    trip = get_object_or_404(Trip, username__username=user.username, id=pk)
    title = trip.title
    start_date = trip.start_date
    end_date = trip.end_date
    
    # 日付のリスト
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)
    
    # フォームセット定義
    ItineraryFormSet = modelformset_factory(
        model=Itinerary,
        form=ItineraryForm,
        extra=0,
        max_num=100,
    )
    
    if request.method=='POST':
        form_sets = []
        for i, date in enumerate(dates, start=1):
            form_set = ItineraryFormSet(request.POST, prefix=f"form_set{str(i)}")
            form_sets.append(form_set)
            
            if form_set.is_valid():
                valid_forms = form_set.save(commit=False)
                for form in valid_forms:
                    form.title =  trip
                    form.username = user
                    form.save()
            else:
                pass
        
        return redirect('tabinoshiori:itinerary', pk=pk)
        
        
    elif request.method=='GET':
        form_sets = []
        for i, date in enumerate(dates, start=1):
            form_sets.append(ItineraryFormSet(queryset=Itinerary.objects.filter(username__username=user.username, title__title=title, date=date), prefix=f"form_set{str(i)}"))
        
        context = {
            "form_sets": form_sets,
            "title": get_object_or_404(Trip, pk=pk),
            "dates": dates,
        }
        
        return render(request, "tabinoshiori/registeritinerary.html", context)