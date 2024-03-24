"""yellow_rhino URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path
from .views import CarList, CarRecordList, CarPriceMileageList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/cars/', CarList.as_view(), name='car-list'),
    path('api/car-records/<str:vin>/', CarRecordList.as_view(), name='car-record-list'),
    path('api/car-price-mileage/', CarPriceMileageList.as_view(), name='car-price-mileage'),
]
