from django.db import models

# Create your models here.

class Passenger(models.Model):
    nid = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return f'Passenger id = {self.id} || {self.username}'


class Payment(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    date = models.DateField(null=True)
    seat_serial = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.passenger.name} | {self.amount} | {self.date}"
    

class Station(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return f'Station id = {self.id} || {self.name} situated in {self.location}'


class Train(models.Model):
    source = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="source")
    destination = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="destination")
    departure = models.DateTimeField(null=True)
    tickets_available_from = models.DateField(null=True)

    def __str__(self):
        return f'{self.id} | {self.source.location} | {self.destination.location} | {self.departure.strftime("%Y-%m-%d %I:%M %p")}'


class Car(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    car_type = models.CharField(max_length=255)
    fare = models.DecimalField(max_digits=7, decimal_places=2)
    number_of_seats = models.IntegerField(default=20)

    def __str__(self):
        return f'{self.train.id} | {self.car_type} | {self.fare} | {self.number_of_seats}'


class Seat(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    watching_by = models.IntegerField(default=0)
    bought_by = models.ForeignKey(Passenger, on_delete=models.CASCADE, null=True)
    is_sold = models.BooleanField(default=False)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'Seat id = {self.id} || Part of car with car id {self.car.id} which is a part of train with train id {self.car.train.id}'


class Admin(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, null=True)
    is_super = models.BooleanField(default=False)

    def __str__(self):
        return f'Admin id = {self.id} || {self.username}'
