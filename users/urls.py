from django.urls import path
from .views import *

app_name = "users"


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('settings/', ProfileSettingsView.as_view(), name='settings'),
    path('client-profile/<int:pk>/', ProfileView.as_view(), name='profile'),
]