from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('signup/', views.MySignup.as_view(), name='signup'),
    path('login/', views.MyLogin.as_view(), name='login'),
    path('logout/', views.MyLogout.as_view(), name='logout'),
    path('user/', views.MyUser.as_view(), name='user'),
    path('other/', views.MyOther.as_view(), name='other'),
]
