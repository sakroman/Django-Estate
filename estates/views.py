from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.views.generic import DetailView, ListView, View
from estates.models import Estate, Wishlist

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
            if min_bedrooms == '5+':
                queryset = queryset.filter(bedrooms__gte=4)
            else:
                queryset = queryset.filter(bedrooms__gte=min_bedrooms)
        
        if max_bedrooms:
            queryset = queryset.filter(bedrooms__lte=max_bedrooms)

        if min_bathrooms:
            if min_bathrooms == '4+':
                queryset = queryset.filter(bathrooms__gte=4)
            else:
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

class PropertyDetailsView(DetailView):
    model = Estate
    template_name = 'estates/listing_details.html'
    context_object_name = 'listing'

class ContactView(View):
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')
        recipient_email = 'sakroitel300@example.com' 

        send_mail(
            subject=f'New Inquiry from {name}',
            message=f'From: {name}\nEmail: {email}\n\n{message}',
            from_email=email,
            recipient_list=[recipient_email],
            fail_silently=False,
        )

        return JsonResponse({'success': True})

class WishlistView(ListView):
    model = Estate
    template_name = 'estates/wishlist.html'
    context_object_name = 'listings'

    def get_queryset(self):

        wishlist, _ = Wishlist.objects.get_or_create(user=self.request.user)
        products = wishlist.products.all()
        return super().get_queryset()
