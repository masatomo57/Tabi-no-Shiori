from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class MyHome(LoginRequiredMixin, TemplateView):
    template_name = 'tabinoshiori/home.html'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context