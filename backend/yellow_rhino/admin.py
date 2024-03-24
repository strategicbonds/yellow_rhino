from django.contrib import admin
from .models import Car, CarRecord  # Ensure Car is also imported if not already

admin.site.register(Car)
admin.site.register(CarRecord)
