from django.urls import path
from . import views

app_name = 'tabinoshiori'

urlpatterns = [
    path('home/', views.MyHome.as_view(), name='home'),
]