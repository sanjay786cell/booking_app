from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Flight
from .serializers import FlightSerializer
from datetime import datetime

class FlightSearchAPIView(APIView):
    def get(self, request):
        source = request.GET.get('source')
        destination = request.GET.get('destination')
        date = request.GET.get('date')  # YYYY-MM-DD
        sort = request.GET.get('sort')  # price

        flights = Flight.objects.all()

        if source:
            flights = flights.filter(source__iexact=source.strip())

        if destination:
            flights = flights.filter(destination__iexact=destination.strip())

        if date:
            try:
                date_obj = datetime.strptime(date, "%Y-%m-%d").date()
                flights = flights.filter(departure_time__date=date_obj)
            except ValueError:
                return Response(
                    {"error": "Invalid date format. Use YYYY-MM-DD"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if sort == "price":
            flights = flights.order_by("price")

        serializer = FlightSerializer(flights, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
