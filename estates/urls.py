from django.urls import path
from .views import *

app_name = "estates"


urlpatterns = [
    path('property-listings', PropertyListingsView.as_view(), name='listings'),
]