from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Car, CarRecord
from .serializers import CarSerializer, CarRecordSerializer
from django.db.models import F

class CarList(APIView):
    def get(self, request, format=None):
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)

class CarRecordList(APIView):
    def get(self, request, vin, format=None):
        car = Car.objects.get(vin=vin)
        records = CarRecord.objects.filter(car=car)
        serializer = CarRecordSerializer(records, many=True)
        return Response(serializer.data)

class CarPriceMileageList(APIView):
    def get(self, request, format=None):
        # Fetch CarRecord objects with related Car data
        records = CarRecord.objects.select_related('car').all()

        # Prepare data including car details, mileage, and price from CarRecord
        data = [{
            'vin': record.car.vin,
            'make': record.car.make,
            'model': record.car.model,
            'year': record.car.year,
            'mileage': record.mileage, 
            'price': record.price
        } for record in records]

        return Response(data)


