from django.shortcuts import render

from django.views.generic import ListView
from estates.models import Estate

class PropertyListingsView(ListView):
    model = Estate
    template_name = 'estates/listings.html'
    context_object_name = 'listings'

    def get_context_data(self, **kwargs):
        context  = super().get_context_data(**kwargs)
        context['property_types'] = Estate.PROPERTY_TYPES
        context['listing_types'] = Estate.LISTING_TYPES
        return context