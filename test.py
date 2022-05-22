import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'railway_ticketing_system.settings')
import django
django.setup()

import datetime

class Test1:
    @classmethod
    def as_view(cls):
        return cls().respond


class Test2(Test1):

    def respond(self, x, y):
        print(f"x+y={x+y}")

