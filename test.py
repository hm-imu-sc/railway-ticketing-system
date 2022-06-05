import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'railway_ticketing_system.settings')
import django
django.setup()

import datetime

def x(a, b):
    print(a+b)

x(*[int(v) for v in "10:1".split(":")])