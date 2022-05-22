
from my_modules.base_views import TemplateContextView, NoTemplateView
from main.models import Station, Passenger, Admin
from django.shortcuts import render,redirect
from datetime import datetime, timedelta
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

        try:
            Passenger.objects.create(
                nid         = nid,
                name        = name,
                email       = email,
                username    = username,
                password    = sha256(password.encode("ASCII")).hexdigest()
            )
        except:
            return

    def get_redirection(self):
        return 'main:passenger_registration_page'


class LoginPage(TemplateContextView):
    
    def get_context(self, request, *args, **kwargs):
        return {
            'session': {
                'login_error': ''
            }, 
            'old_info': {
                'username': '',
                'password': ''
            }
        }

    def get_template(self):
        return 'login_page.html'


class Login(NoTemplateView):
    
    def act(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        domain = None

        user = list(Passenger.objects.filter(username__exact=username))

        if len(user) == 1:
            user = user[0]
            domain = "passenger"
        else:
            user = list(Admin.objects.filter(username__exact=username))        
            if len(user) == 1:
                user = user[0]
                domain = "admin"

        if domain is not None:
            if self.__veryfy_password(user, password):
                request.session['user'] = {
                    'login_status': True,
                    'username': username,
                    'domain': domain
                }
                self.redirect_to = 'main:home_page'
                request.session['login_error'] = ''
            else:
                self.redirect_to = 'main:login_page'
                request.session['login_error'] = 'error'
                request.session['old_info'] = {
                    'username': username,
                    'password': password
                }
        else:
            self.redirect_to = 'main:login_page'
            request.session['login_error'] = 'error'
            request.session['old_info'] = {
                'username': username,
                'password': password
            }

    def get_redirection(self):
        return self.redirect_to

    def __veryfy_password(self, user, password):
        return sha256(password.encode('ascii')).hexdigest() == user.password        


class Logout(NoTemplateView):
    def act(self, request, *args, **kwargs):
        request.session['user'] = {'login_status': False}
        try:
            del request.session['login_error']
            del request.session['old_info']
        except KeyError:
            return

    def get_redirection(self):
        return 'main:login_page'


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



