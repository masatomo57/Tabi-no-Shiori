from django.urls import path
from . import views
from django.views.generic import RedirectView

app_name = 'tabinoshiori'

urlpatterns = [
    path('', RedirectView.as_view(url='/home/')),
    path('home/', views.HomeView, name='home'),
    path('trip/register', views.RegisterTripView.as_view(), name='registertrip'),
    path('trip/delete', views.DeleteTripView, name="deletetrip"),
    path('itinerary/<int:pk>/register/', views.RegisterItineraryView, name='registeritinerary'),
    path('itinerary/<int:pk>/', views.ItineraryView, name='itinerary'),
]