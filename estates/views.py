from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import ListView
from estates.models import Estate

class PropertyListingsView(ListView):
    model = Estate
    template_name = 'estates/listings.html'
    context_object_name = 'listings'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        property_type = self.request.GET.get('property_type')
        listing_type = self.request.GET.get('listing_type')
        min_bedrooms = self.request.GET.get('min_bedrooms')
        max_bedrooms = self.request.GET.get('max_bedrooms')
        min_bathrooms = self.request.GET.get('min_bathrooms')
        max_bathrooms = self.request.GET.get('max_bathrooms')
        has_garage = self.request.GET.get('has_garage')
        has_garden = self.request.GET.get('has_garden')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')

        if search_query:
            queryset = queryset.filter(
                Q(address__icontains=search_query) |
                Q(city__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        if property_type and property_type != 'All':
            queryset = queryset.filter(property_type=property_type)

        if listing_type and listing_type != 'All':
            queryset = queryset.filter(listing_type=listing_type)
            
        if min_bedrooms:
            queryset = queryset.filter(bedrooms__gte=min_bedrooms)
        
        if max_bedrooms:
            queryset = queryset.filter(bedrooms__lte=max_bedrooms)

        if min_bathrooms:
            queryset = queryset.filter(bathrooms__gte=min_bathrooms)
        
        if max_bathrooms:
            queryset = queryset.filter(bathrooms__lte=max_bathrooms)

        if has_garage:
            queryset = queryset.filter(garage=True)

        if has_garden:
            queryset = queryset.filter(garden=True)
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        return queryset.distinct()


    def get_context_data(self, **kwargs):
        context  = super().get_context_data(**kwargs)
        context['property_types'] = Estate.PROPERTY_TYPES
        context['listing_types'] = Estate.LISTING_TYPES
        return context