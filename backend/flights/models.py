from django.db import models

class Flight(models.Model):
    flight_number = models.CharField(max_length=20)
    source = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()

    def save(self, *args, **kwargs):
        self.source = self.source.strip().upper()
        self.destination = self.destination.strip().upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.flight_number
