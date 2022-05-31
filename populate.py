import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'railway_ticketing_system.settings')
import django
django.setup()

from main.models import Station, Train, Car, Seat




