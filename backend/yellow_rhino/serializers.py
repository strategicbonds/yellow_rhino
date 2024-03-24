from rest_framework import serializers
from .models import Car, CarRecord

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['vin', 'make', 'model', 'year', 'fuel_type', 'packages', 'drive_type', 'engine', 'color_ext', 'color_int', 'transmission', 'trim']

class CarRecordSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)
    
    class Meta:
        model = CarRecord
        fields = ['car', 'price', 'mileage', 'date', 'source']
