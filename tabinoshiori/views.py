from django.forms.models import modelformset_factory
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from tabinoshiori.models import Trip, Itinerary
from tabinoshiori.forms import TripForm, ItineraryForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render, get_list_or_404
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


@login_required
def ItineraryView(request, pk):
    user = request.user
    trip = Trip.objects.get(username__username=user.username, id=pk)
    start_date = trip.start_date
    end_date = trip.end_date
    
    itinerarys_list = []
    dates = Itinerary.objects.filter(username__username=user.username, title__title=trip.title).order_by("date").distinct().values_list("date", flat=True)
    for date in dates:
        itinerarys_list.append(Itinerary.objects.filter(username__username=user.username, title__title=trip.title, date=date).order_by("start_time"))
    
    context = {
        "title": trip.title,
        "id": trip.id,
        "itinerarys_list": itinerarys_list,
        "dates": dates,
        "start_date": start_date,
        "end_date": end_date,
    }
    return render(request, 'tabinoshiori/trip.html', context)
    

class RegisterTripView(LoginRequiredMixin, CreateView):
    model = Trip
    form_class = TripForm
    template_name = 'tabinoshiori/registertrip.html'
    success_url = reverse_lazy('tabinoshiori:home')
    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)


@login_required
def DeleteTripView(request):
    user = request.user
    trip_list = get_list_or_404(Trip, username__username=user.username)
    
    if request.method=='POST':
        for trip in trip_list:
            if f"is_delete{trip.id}" in request.POST:
                trip.delete()
        
        return redirect('tabinoshiori:deletetrip')
    elif request.method=='GET':
        context = {
            "trip_list": trip_list
        }
        return render(request, "tabinoshiori/deletetrip.html", context)


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
        for i, date in enumerate(dates, start=1):
            form_set = ItineraryFormSet(request.POST, prefix=f"form_set{str(i)}")
            if form_set.is_valid():
                valid_forms = form_set.save(commit=False)
                for form in valid_forms:
                    form.title =  trip
                    form.username = user
                    form.save()
            else:
                pass
            
            form_set_num = int(request.POST.get(f'form_set{i}-TOTAL_FORMS'))
            for j in range(form_set_num):
                if f"form_set{i}-{j}-is_delete" in request.POST:
                    delete_id = request.POST.get(f'form_set{i}-{j}-id')
                    if not delete_id is '':
                        get_object_or_404(Itinerary, pk=int(delete_id)).delete()
                    else:
                        get_object_or_404(Itinerary, username__username=user.username, title__title=title, action=request.POST.get(f'form_set{i}-{j}-action'), date=request.POST.get(f'form_set{i}-{j}-date'), start_time=request.POST.get(f'form_set{i}-{j}-start_time'), end_time=request.POST.get(f'form_set{i}-{j}-end_time')).delete()
            
        return redirect('tabinoshiori:itinerary', pk=pk)
        
        
    elif request.method=='GET':
        form_sets = []
        for i, date in enumerate(dates, start=1):
            append_form_set = ItineraryFormSet(queryset=Itinerary.objects.filter(username__username=user.username, title__title=title, date=date), prefix=f"form_set{str(i)}")
            form_sets.append(append_form_set)
    
        
        context = {
            "form_sets": form_sets,
            "title": get_object_or_404(Trip, pk=pk),
            "dates": dates,
        }
        
        return render(request, "tabinoshiori/registeritinerary.html", context)