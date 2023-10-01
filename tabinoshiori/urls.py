from django.urls import path
from . import views
from django.views.generic import RedirectView

app_name = 'tabinoshiori'

urlpatterns = [
    path('', RedirectView.as_view(url='/home/')),
    path('home/', views.HomeView, name='home'),
    path('register/trip/', views.RegisterTripView.as_view(), name='registertrip'),
    path('itinerary/<int:pk>/register/', views.RegisterItineraryView, name='registeritinerary'),
    path('itinerary/<int:pk>/', views.ItineraryView, name='itinerary'),
]