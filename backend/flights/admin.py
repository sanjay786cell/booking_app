from django.contrib import admin
from .models import Flight

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = (
        "flight_number",
        "source",
        "destination",
        "departure_time",
        "price",
        "available_seats",
    )
    search_fields = ("flight_number", "source", "destination")
    list_filter = ("source", "destination")
