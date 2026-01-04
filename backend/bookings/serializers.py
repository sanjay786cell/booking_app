from rest_framework import serializers
from .models import Booking

"""
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ("user", "status", "booking_time")
"""

from rest_framework import serializers
from .models import Booking
from flights.models import Flight

class FlightMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = (
            "id",
            "flight_number",
            "source",
            "destination",
            "price",
        )

class BookingSerializer(serializers.ModelSerializer):
    flight = FlightMiniSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = (
            "id",
            "flight",
            "status",
            "booking_time",
        )
