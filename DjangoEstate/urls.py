
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from .views import *
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('user/', include('users.urls')),
    path('estate/', include('estates.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
