from django.db import models

# Create your models here.

class Admin(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

class Passenger(models.Model):
    nid = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

class Station(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)

class Train(models.Model):
    source = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="source")
    destination = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="destination")
    departure = models.DateTimeField(null=True)
    tickets_available_from = models.DateField(null=True)

class Car(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    car_type = models.CharField(max_length=255)
    fare = models.DecimalField(max_digits=7, decimal_places=2)
    number_of_seats = models.IntegerField(default=20)

class Seat(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    watching_by = models.IntegerField(default=0)
    bought_by = models.ForeignKey(Passenger, on_delete=models.CASCADE, null=True)
    is_sold = models.BooleanField(default=False)
