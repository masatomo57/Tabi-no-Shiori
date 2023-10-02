from .forms import SignupForm, LoginForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

class MySignup(CreateView):
    template_name = 'account/signup.html'
    form_class = SignupForm
    success_url = '/account/login/'
    
    def form_valid(self, form):
        result = super().form_valid(form)
        user = self.object
        login(self.request, user)
        return result

class MyLogin(LoginView):
    template_name = 'account/login.html'
    form_class = LoginForm

class MyLogout(LogoutView):
    template_name = 'account/logout.html'

class MyUser(LoginRequiredMixin, TemplateView):
    template_name = 'account/user.html'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class MyOther(LoginRequiredMixin, TemplateView):
    template_name = 'account/other.html'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['users']= User.objects.exclude(username=self.request.user.username)
        return context