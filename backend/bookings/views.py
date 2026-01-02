from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db import transaction
from django.shortcuts import get_object_or_404
from .models import Booking
from .serializers import BookingSerializer
from flights.models import Flight

class BookFlightAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        flight_id = request.data.get("flight_id")

        if not flight_id:
            return Response(
                {"error": "flight_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            flight = Flight.objects.select_for_update().get(id=flight_id)
        except Flight.DoesNotExist:
            return Response(
                {"error": "Flight not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if flight.available_seats <= 0:
            return Response(
                {"error": "No seats available"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Reduce seat
        flight.available_seats -= 1
        flight.save()

        booking = Booking.objects.create(
            user=request.user,
            flight=flight,
            status="CONFIRMED"
        )

        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MyBookingsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(
            user=request.user
        ).select_related("flight").order_by("-booking_time")

        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

class CancelBookingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, booking_id):
        booking = get_object_or_404(
            Booking,
            id=booking_id,
            user=request.user
        )

        if booking.status == "CANCELLED":
            return Response(
                {"error": "Booking already cancelled"},
                status=status.HTTP_400_BAD_REQUEST
            )

        flight = booking.flight

        # Lock flight row
        flight = Flight.objects.select_for_update().get(id=flight.id)

        # Restore seat
        flight.available_seats += 1
        flight.save()

        booking.status = "CANCELLED"
        booking.save()

        return Response(
            {"message": "Booking cancelled successfully"},
            status=status.HTTP_200_OK
        )