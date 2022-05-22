
from my_modules.base_views import TemplateContextView, NoTemplateView
from main.models import Station, Passenger, Admin, Train, Car, Seat
from django.shortcuts import render,redirect
from datetime import datetime, timedelta
from hashlib import sha256
import zoneinfo
from django.utils.dateparse import parse_datetime


class HomePage(TemplateContextView):
    
    def get_context(self, request, *args, **kwargs):
        stations = list(Station.objects.all())

        day_seq = {}
        days = ['Fri', 'Sat', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu']

        for i in range(7):
            day_seq[days[i]] = i

        today_x = datetime.now()
        x = datetime.now()
        today = int(x.day)

        weekend = today - day_seq[x.strftime("%a")]

        x -= timedelta(days=day_seq[x.strftime("%a")])

        return {
            'stations': [station.location for station in stations],
            'week_0': [
                {
                    'day': day, 
                    'date': weekend+day_seq[day],
                    'full_date': f"{(x+timedelta(days=day_seq[day])).day}-{(x+timedelta(days=day_seq[day])).month}-{(x+timedelta(days=day_seq[day])).year}",
                    'backdate': (x+timedelta(days=day_seq[day])) < today_x,
                }
                for day in day_seq.keys()
            ],
            'week_1': [
                {
                    'day': day, 
                    'date': (x+timedelta(days=7+day_seq[day])).day,
                    'full_date': f"{(x+timedelta(days=7+day_seq[day])).day}-{(x+timedelta(days==7+day_seq[day])).month}-{(x+timedelta(days==7+day_seq[day])).year}",
                    'backdate': (x+timedelta(days=7+day_seq[day])) < today_x,
                }
                for day in day_seq.keys()
            ],
            'week_2': [
                {
                    'day': day, 
                    'date': (x+timedelta(days=14+day_seq[day])).day,
                    'full_date': f"{(x+timedelta(days=14+day_seq[day])).day}-{(x+timedelta(days=14+day_seq[day])).month}-{(x+timedelta(days=14+day_seq[day])).year}",
                    'backdate': (x+timedelta(days=14+day_seq[day])) < today_x,
                }
                for day in day_seq.keys()
            ],
            'today': today,
        }

    def get_template(self):
        return 'home_page.html'


class SeatSelectionPage(TemplateContextView):
    def get_context(self, request, *args, **kwargs):
        train_id = kwargs['trian_id']
        return {}

    def get_template(self):
        pass


class GetSchedule(TemplateContextView):

    def get_context(self, request, *args, **kwargs):
        date = kwargs['date']
        source = kwargs['source']
        destination = kwargs['destination']

        train_schedules = []

        for train in Train.objects.all():

            if f'{train.departure.day}-{train.departure.month}-{train.departure.year}' == date and train.source.location == source and train.destination.location == destination:
                seats = 0
                booked = 0

                for car in train.car_set.all():
                    seats += car.number_of_seats
                    for seat in car.seat_set.all():
                        booked += seat.is_sold
            
                booked_percent = 0 if booked == 0 else int(seats/booked)*100
                booked_class = ''

                if seat == booked:
                    booked_class = 'status_100'
                elif booked_percent >= 75:
                    booked_class = 'status_75'
                elif booked_percent >= 50:
                    booked_class = 'status_50'
                elif booked_percent >= 25:
                    booked_class = 'status_25'
                else:
                    booked_class = 'status_0'

                train_schedules.append({
                    'train_id': train.id,
                    'source': source,
                    'destination': destination,
                    'time': train.departure.strftime("%I:%M %p"),
                    'fare_range': {
                        'max': train.car_set.all().order_by('-fare')[0].fare,
                        'min': train.car_set.all().order_by('fare')[0].fare,
                    },
                    'seat_status': booked_class,
                })

        return {
            'train_schedules': train_schedules
        }

    def get_template(self):
        return 'train_schedules.html'


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

class AddStation(NoTemplateView):
    def act(self, request, *args, **kwargs):
        if request.method == 'POST':
            st_name=request.POST.get('station_name')
            st_location=request.POST.get('station_location')
            st_description=request.POST.get('station_description')
            station = Station.objects.create(
                name=st_name,location=st_location,description=st_description
            )
    def get_redirection(self):
        return 'main:add_station_page'

class AddTrainPage(TemplateContextView):
    def get_context(self, request, *args, **kwargs):
        print('in add_train_page')
        context = {}
        context['stations'] = Station.objects.all()
        return context
    def get_template(self):
        return 'add_train.html'

class AddTrain(NoTemplateView):
    def act(self, request, *args, **kwargs):
        print('in add_train')
        f_berthNOS = 6 * 4
        f_seatNOS = 14 * 4
        s_chairNOS = 14 * 4
        shovanNOS = 16 * 4
        if request.method == 'POST':
            fr = request.POST.get('from')
            to = request.POST.get('to')
            f_berth = request.POST.get('f_berth')
            f_seat = request.POST.get('f_seat')
            s_chair = request.POST.get('s_chair')
            shovan = request.POST.get('shovan')
            f_berth_fare = request.POST.get('f_berth_fare')
            f_seat_fare = request.POST.get('f_seat_fare')
            s_chair_fare = request.POST.get('s_chair_fare')
            shovan_fare = request.POST.get('shovan_fare')
            dept_time = request.POST.get('dept_date')

            # adding train
            source_station = Station.objects.filter(id=fr)[0]
            des_station = Station.objects.filter(id=to)[0]
            dept_time = dept_time.replace('T', ' ')
            dept_time = parse_datetime(dept_time)
            dept_time = dept_time.replace(tzinfo=zoneinfo.ZoneInfo('Asia/Dhaka'))
            # print(dept_time)
            # print(f'dept_time is type {type(dept_time)}')
            opening_date = dept_time - timedelta(days=7)
            # print(opening_date)
            # print(f'opening_date is type {type(opening_date)}')
            new_train = Train.objects.create(
                source=source_station, destination=des_station, departure=dept_time, tickets_available_from=opening_date
            )

            # adding car and seats
            for i in range(int(f_berth)):
                new_car = Car.objects.create(
                    train=new_train, car_type='f_berth', fare=int(f_berth_fare), number_of_seats=int(f_berthNOS)
                )
                for j in range(int(f_berthNOS)):
                    new_seat = Seat.objects.create(
                        car=new_car
                    )

            for i in range(int(f_seat)):
                new_car = Car.objects.create(
                    train=new_train, car_type='f_seat', fare=int(f_seat_fare), number_of_seats=int(f_seatNOS)
                )
                for j in range(int(f_seatNOS)):
                    new_seat = Seat.objects.create(
                        car=new_car
                    )

            for i in range(int(s_chair)):
                new_car = Car.objects.create(
                    train=new_train, car_type='s_chair', fare=int(s_chair_fare), number_of_seats=int(s_chairNOS)
                )
                for j in range(int(s_chairNOS)):
                    new_seat = Seat.objects.create(
                        car=new_car
                    )

            for i in range(int(shovan)):
                new_car = Car.objects.create(
                    train=new_train, car_type='shovan', fare=int(shovan_fare), number_of_seats=int(shovanNOS)
                )
                for j in range(int(shovanNOS)):
                    new_seat = Seat.objects.create(
                        car=new_car
                    )
    def get_redirection(self):
        return 'main:add_train_page'




