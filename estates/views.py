import json
from django.core import paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, request
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, View
from estates.models import Estate, SavedSearch, Wishlist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class PropertyListingsView(ListView):
    model = Estate
    template_name = 'estates/listings.html'
    context_object_name = 'listings'
    paginate_by = 3

    def get_ordering(self):
        sort_option = self.request.GET.get('sort')

        if sort_option == 'price_asc':
            return ['price']
        elif sort_option == 'price_desc':
            return ['-price']

        return []

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search_query')
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

        return queryset.distinct().order_by(*self.get_ordering())

    def get_context_data(self, **kwargs):
        context  = super().get_context_data(**kwargs)
        paginator = Paginator(context['listings'], self.paginate_by)
        page = self.request.GET.get('page')

        try:
            listings = paginator.page(page)
        except PageNotAnInteger:
            listings = paginator.page(1)
        except EmptyPage:
            listings = paginator.page(paginator.num_pages)

        if self.request.user.is_authenticated:
            current_search_criteria = {
            'search': self.request.GET.get('search_query', ''),
            'property_type':  self.request.GET.get('property_type', ''),
            'listing_type':  self.request.GET.get('listing_type', ''),
            'min_bedrooms':  self.request.GET.get('min_bedrooms'),
            'max_bedrooms':  self.request.GET.get('max_bedrooms'),
            'min_bathrooms':  self.request.GET.get('min_bathrooms'),
            'max_bathrooms':  self.request.GET.get('max_bathrooms'),
            'garage':  self.request.GET.get('has_garage', False),
            'garden':  self.request.GET.get('has_garden', False),

            }
            is_search_saved = SavedSearch.objects.filter(user=self.request.user, **current_search_criteria).exists()
            context['is_search_saved'] = is_search_saved
        context['listings'] = listings
        context['property_types'] = Estate.PROPERTY_TYPES
        context['listing_types'] = Estate.LISTING_TYPES
        return context



class PropertyDetailsView(DetailView):
    model = Estate
    template_name = 'estates/listing_details.html'
    context_object_name = 'listing'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            wishlist, _ = Wishlist.objects.get_or_create(user=self.request.user)
            wishlisted = self.object in wishlist.estates.all()
            context['is_wishlisted'] = wishlisted
        return context

class ContactView(LoginRequiredMixin, View):
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

class WishlistView(LoginRequiredMixin, ListView):
    model = Estate
    template_name = 'estates/wishlist.html'
    context_object_name = 'listings'

    def get_ordering(self):
        sort_option = self.request.GET.get('sort')
        print(sort_option)
        if sort_option == 'price_asc':
            return ['price']
        elif sort_option == 'price_desc':
            return ['-price']

        return super().get_ordering()


    def get_queryset(self):
        wishlist, _ = Wishlist.objects.get_or_create(user=self.request.user)
        queryset = wishlist.estates.all()
        ordering = self.get_ordering()
        if ordering:
            queryset = queryset.order_by(*ordering)
        return queryset


class AddRemoveWishlistView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        estate_id = json.loads(request.body)

        estate = get_object_or_404(Estate, id=estate_id)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        if estate not in wishlist.estates.all():
            wishlist.estates.add(estate)
            added = True
        else:
            wishlist.estates.remove(estate)
            added = False

        return JsonResponse({'added': added})


class SavedSearchesPageView(LoginRequiredMixin, ListView):
    model = SavedSearch
    template_name = 'estates/saved-searches.html'
    context_object_name = 'searches'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.request.user.savedsearch_set.all()
        
        return queryset


class SaveSearchView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        search_criteria = json.loads(body_unicode)
        min_price = search_criteria.get('minPrice')
        max_price = search_criteria.get('maxPrice')

        min_price = int(min_price) if min_price else None
        max_price = int(max_price) if max_price else None

        existing_search = SavedSearch.objects.filter(
            user=request.user,
            search=search_criteria.get('search'),
            property_type=search_criteria.get('property_type'),
            listing_type=search_criteria.get('listing_type'),
            min_bedrooms=search_criteria.get('minBedrooms'),
            max_bedrooms=search_criteria.get('maxBedrooms'),
            min_bathrooms=search_criteria.get('minBathrooms'),
            max_bathrooms=search_criteria.get('maxBathrooms'),
            garage=search_criteria.get('garage'),
            garden=search_criteria.get('garden'),
            minPrice=min_price,
            maxPrice=max_price,
        ).first()

        if existing_search:
            existing_search.delete()
            return JsonResponse({'message': 'Search removed successfully'})
        else:
            SavedSearch.objects.create(
                user=request.user,
                search=search_criteria.get('search'),
                property_type=search_criteria.get('property_type'),
                listing_type=search_criteria.get('listing_type'),
                min_bedrooms=search_criteria.get('minBedrooms'),
                max_bedrooms=search_criteria.get('maxBedrooms'),
                min_bathrooms=search_criteria.get('minBathrooms'),
                max_bathrooms=search_criteria.get('maxBathrooms'),
                garage=search_criteria.get('garage'),
                garden=search_criteria.get('garden'),
                minPrice=min_price,
                maxPrice=max_price,
            )
            return JsonResponse({'message': 'Search saved successfully'})


class DeleteSearchView(LoginRequiredMixin, DeleteView):
    model = SavedSearch
    success_url = reverse_lazy('estates:saved-searches')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'message': 'Search deleted successfully'})