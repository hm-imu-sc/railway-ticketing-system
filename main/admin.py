from django.contrib import admin
from .models import Passenger, Train, Seat, Car, Station

# Register your models here.

admin.site.register(Passenger)
admin.site.register(Station)
admin.site.register(Train)
admin.site.register(Seat)
admin.site.register(Car)
