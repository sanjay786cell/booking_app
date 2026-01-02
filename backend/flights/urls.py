from django.urls import path
from .views import FlightSearchAPIView

urlpatterns = [
    path('search/', FlightSearchAPIView.as_view(), name='flight-search'),
]
