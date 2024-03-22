from django.urls import path
from .views import *

app_name = "estates"


urlpatterns = [
    path('property-listings', PropertyListingsView.as_view(), name='listings'),
    path('property-details/<int:pk>/', PropertyDetailsView.as_view(), name='property_details'),
    path('user/saved-properties/', WishlistView.as_view(), name='saved-properties'),
    path('user/add-remove-wishlist/', AddRemoveWishlistView.as_view(), name='add-remove-wishlist'),
    path('user/saved-searches/', SavedSearchesPageView.as_view(), name='saved-searches'),
    path('save-search/', SaveSearchView.as_view(), name='save-search'),
    path('delete-search/<int:pk>/', DeleteSearchView.as_view(), name='delete-search'),
    path('contact/', ContactView.as_view(), name='contact'),
]