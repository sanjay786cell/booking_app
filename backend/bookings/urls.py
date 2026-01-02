from django.urls import path
from .views import BookFlightAPIView, MyBookingsAPIView, CancelBookingAPIView

urlpatterns = [
    path('book/', BookFlightAPIView.as_view(), name='book-flight'),
    path('my/', MyBookingsAPIView.as_view(), name='my-bookings'),
    path('cancel/<int:booking_id>/', CancelBookingAPIView.as_view(), name='cancel-booking'),
]
