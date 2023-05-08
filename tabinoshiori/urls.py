from django.urls import path
from . import views

app_name = 'tabinoshiori'

urlpatterns = [
    path('home/', views.MyHome.as_view(), name='home'),
    path('register/trip/', views.MyRegisterTrip.as_view(), name='registertrip'),
    path('itinerary/<int:pk>/', views.MyItineraryView.as_view(), name='itinerary'),
]