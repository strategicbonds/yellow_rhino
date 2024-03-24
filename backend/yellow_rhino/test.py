from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Car

class CarAPITests(APITestCase):
    def test_view_cars(self):
        """
        Ensure we can view the list of cars.
        """
        # Setup - create a car instance
        Car.objects.create(vin="1HGCM82633A004352", make="Honda", model="Accord", year=2020, fuel_type="Gasoline")

        # Make a GET request to the cars endpoint
        url = reverse('car-list')
        response = self.client.get(url, format='json')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response contains our car
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['make'], 'Honda')
