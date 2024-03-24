from django.db import models
from datetime import date

class Car(models.Model):
    vin = models.CharField(max_length=17, unique=True)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    fuel_type = models.CharField(max_length=50)
    packages = models.TextField(blank=True, null=True)
    drive_type = models.CharField(max_length=50)
    engine = models.CharField(max_length=100)
    color_ext = models.CharField(max_length=50)
    color_int = models.CharField(max_length=50)
    transmission = models.CharField(max_length=50)
    trim = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"

class CarRecord(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='records')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    mileage = models.IntegerField()
    date = models.DateField(default=date.today)
    source = models.CharField(max_length=255)

    def __str__(self):
        return f"Record for {self.car} on {self.date}"
