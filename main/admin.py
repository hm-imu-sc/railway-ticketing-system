from django.contrib import admin
from .models import Admin, Passenger, Train, Seat, Car, Station, Payment

# Register your models here.

admin.site.register(Passenger)
admin.site.register(Payment)
admin.site.register(Station)
admin.site.register(Admin)
admin.site.register(Train)
admin.site.register(Seat)
admin.site.register(Car)
