
from django.views.generic import ListView
from estates.models import Estate

class HomeView(ListView):
    model = Estate
    template_name = 'general/home.html'
    ordering = ['-list_date']
    context_object_name = 'estates'