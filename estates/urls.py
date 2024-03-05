from django.urls import path
from .views import *

app_name = "estates"


urlpatterns = [
    path('property-listings', PropertyListingsView.as_view(), name='listings'),
    path('property-details/<int:pk>/', PropertyDetailsView.as_view(), name='property_details'),
]