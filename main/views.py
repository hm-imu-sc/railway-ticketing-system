
from my_modules.base_views import TemplateContextView, NoTemplateView
from main.models import Station, Passenger
from django.shortcuts import render,redirect
from hashlib import sha256

class HomePage(TemplateContextView):
    def get_template(self):
        return 'home_page.html'


class PassengerRegistrationPage(TemplateContextView):
    def get_template(self):
        return 'passenger_registration_page.html'


class PassengerRegistration(NoTemplateView):
    def act(self, request, *args, **kwargs):
        nid = request.POST.get("nid")
        name = request.POST.get("name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        Passenger.objects.create(
            nid         = nid,
            name        = name,
            email       = email,
            username    = username,
            password    = sha256(password.encode("ASCII")).hexdigest()
        )

    def get_redirection(self):
        return 'main:passenger_registration_page'


class LoginPage(TemplateContextView):
    def get_template(self):
        return 'login_page.html'


class AddStationPage(TemplateContextView):
    def get_template(self):
        return 'add_station.html'


def addStation(request):
        if request.method == 'POST':
            st_name=request.POST.get('station_name')
            st_location=request.POST.get('station_location')
            st_description=request.POST.get('station_description')
            station = Station.objects.create(
                name=st_name,location=st_location,description=st_description
            )
            return redirect('main:add_station')
        return render(request,'add_station.html')



