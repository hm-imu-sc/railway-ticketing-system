
from my_modules.base_views import APIOnlyView, TemplateContextView, NoTemplateView, ActionOnlyView
from main.models import Station, Passenger, Admin, Train, Car, Seat
from django.shortcuts import render,redirect
from datetime import datetime, timedelta
from hashlib import sha256
import zoneinfo
from django.utils.dateparse import parse_datetime
import json


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
                    'date': (x+timedelta(days=day_seq[day])).day,
                    'full_date': f"{(x+timedelta(days=day_seq[day])).day}-{(x+timedelta(days=day_seq[day])).month}-{(x+timedelta(days=day_seq[day])).year}",
                    'backdate': (x+timedelta(days=day_seq[day])) < today_x,
                }
                for day in day_seq.keys()
            ],
            'week_1': [
                {
                    'day': day, 
                    'date': (x+timedelta(days=7+day_seq[day])).day,
                    'full_date': f"{(x+timedelta(days=7+day_seq[day])).day}-{(x+timedelta(days=7+day_seq[day])).month}-{(x+timedelta(days==7+day_seq[day])).year}",
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
            'nav': {
                'home_page': 'active'
            }
        }

    def get_template(self):
        return 'home_page.html'


class AdminHomePage(TemplateContextView):
    def get_context(self, request, *args, **kwargs):
        return {
            'nav': {
                'admin_home_page': 'active'
            }
        }

    def get_template(self):
        return 'admin_home_page.html'


class SeatSelectionPage(TemplateContextView):
    def get_context(self, request, *args, **kwargs):
        train_id = kwargs['train_id']
        train = Train.objects.get(id=train_id)
        return {
            'cars': [
                {
                    'id': '1',
                    'name': 'First Class Berth',
                    'fare': '1500',
                },
                {
                    'id': '2',
                    'name': 'First Class Seat',
                    'fare': '1250',
                },
                {
                    'id': '3',
                    'name': 'Shovan Chair',
                    'fare': '750',
                },
                {
                    'id': '4',
                    'name': 'Shovan',
                    'fare': '500',
                },
            ]
        }

    def get_template(self):
        return 'seat_selection_page.html'


class GetSchedule(TemplateContextView):

    def get_context(self, request, *args, **kwargs):
        date = kwargs['date']
        source = kwargs['source']
        destination = kwargs['destination']

        train_schedules = []

        for train in Train.objects.all():

            # print(f'{train.departure.day}-{train.departure.month}-{train.departure.year} | {date}')

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
    
    def get_context(self, request, *args, **kwargs):
        return {
            'nav': {
                'registration_page': 'active'
            }
        }

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
                # request.session.set_expire(timedelta(days=1))

                if domain == 'admin':
                    self.redirect_to = 'main:admin_home_page'
                else:
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


class AddStation(ActionOnlyView):
    def act(self, request, *args, **kwargs):

        st_name = kwargs['name']
        st_location = kwargs['location']
        st_description = kwargs['desc']

        try:
            Station.objects.create(
                name=st_name,
                location=st_location,
                description=st_description
            )
            return json.dumps({
                'status': True,
                'message': 'Station added successfully !!!'
            })

        except:
            return json.dumps({
                'status': False,
                'message': 'Couldn\'t add station !!!'
            })


class AddTrainPage(TemplateContextView):
    def get_context(self, request, *args, **kwargs):
        return {
            'stations': Station.objects.all(),
            'current_datetime': datetime.today().strftime("%Y-%m-%dT%H:%M")
        }

    def get_template(self):
        return 'add_train.html'


class AddTrain(ActionOnlyView):
    def act(self, request, *args, **kwargs):

        f_berthNOS = 6 * 4
        f_seatNOS = 10 * 4
        s_chairNOS = 10 * 4
        shovanNOS = 14 * 4
        
        if request.method == 'GET':
            fr = request.GET.get('from')
            to = request.GET.get('to')
            f_berth = request.GET.get('f_berth')
            f_seat = request.GET.get('f_seat')
            s_chair = request.GET.get('s_chair')
            shovan = request.GET.get('shovan')
            f_berth_fare = request.GET.get('f_berth_fare')
            f_seat_fare = request.GET.get('f_seat_fare')
            s_chair_fare = request.GET.get('s_chair_fare')
            shovan_fare = request.GET.get('shovan_fare')
            dept_time = request.GET.get('dept_date')

            print(f'Departure: {dept_time}')

            source_station = Station.objects.filter(id=fr)[0]
            des_station = Station.objects.filter(id=to)[0]

            dept_time = dept_time.replace('T', ' ')
            dept_time = parse_datetime(dept_time)
            dept_time = dept_time.replace(tzinfo=zoneinfo.ZoneInfo('Asia/Dhaka'))
            opening_date = dept_time - timedelta(days=7)

            new_train = Train.objects.create(
                source=source_station, destination=des_station, departure=dept_time, tickets_available_from=opening_date
            )

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
    
            return json.dumps({
                "status": True,
                "message": "Train added successfully !!!"
            })
        else:
            return json.dumps({
                "status": False,
                "message": "Error adding train !!!"
            })


class SchedulerPage(TemplateContextView):

    def get_context(self, request, *args, **kwargs):
        return {
            "railway_name": Admin.objects.get(username=request.session['user']['username']).station.name
        }

    def get_template(self):
        return "scheduler_page.html"


class DaySchedule(TemplateContextView):

    def get_context(self, request, *args, **kwargs):
        
        station_id = Admin.objects.get(username=request.session['user']['username']).station.id
        
        file = open(f'json/default_day_schedule_{station_id}.json', 'r')
        day_schedule = json.load(file)
        file.close()

        next_id = 0

        for schedule in day_schedule:
            next_id = max(next_id, schedule['id'])

        if request.method == "GET":
            context = {
                "schedules": []
            }

            for schedule in day_schedule:

                schedule['source'] = Station.objects.get(id=int(schedule['source'])).location
                schedule['destination'] = Station.objects.get(id=int(schedule['destination'])).location
                context['schedules'].append(schedule)

            return context
        else:

            schedule = {
                'id': next_id+1,
                'source': request.POST.get('source'),
                'destination': request.POST.get('dest'),
                'time': request.POST.get('dept'),
                'cars': [
                    {
                        'type': 'First Class Birth',
                        'number_of_cars': int(request.POST.get('fcb')),
                        'seats_per_car': 24,
                        'fare': int(request.POST.get('fcb_fare'))
                    },
                    {
                        'type': 'First Class Seat',
                        'number_of_cars': int(request.POST.get('fcs')),
                        'seats_per_car': 40,
                        'fare': int(request.POST.get('fcs_fare'))
                    },
                    {
                        'type': 'Shovan Chair',
                        'number_of_cars': int(request.POST.get('sc')),
                        'seats_per_car': 40,
                        'fare': int(request.POST.get('sc_fare'))
                    },
                    {
                        'type': 'Shovan',
                        'number_of_cars': int(request.POST.get('s')),
                        'seats_per_car': 56,
                        'fare': int(request.POST.get('s_fare'))
                    },
                ]
            }

            day_schedule.append(schedule)

            file = open(f'json/default_day_schedule_{station_id}.json', 'w')
            json.dump(day_schedule, file)
            file.close()

            schedule['source'] = Station.objects.get(id=int(schedule['source'])).location
            schedule['destination'] = Station.objects.get(id=int(schedule['destination'])).location

            return {
                "schedules": [schedule]
            }

    def get_template(self):
        return "schedule.html"


class DeleteDaySchedule(ActionOnlyView):
    def act(self, request, *args, **kwargs):
        to_delete = kwargs['id']
        
        station_id = Admin.objects.get(username=request.session['user']['username']).station.id

        file = open(f'json/default_day_schedule_{station_id}.json', 'r')
        all_schedules = json.load(file)
        file.close()

        file = open(f'json/default_day_schedule_{station_id}.json', 'w')
        
        for i in range(len(all_schedules)):
            if all_schedules[i]['id'] == to_delete:
                all_schedules.remove(all_schedules[i])        

                json.dump(all_schedules, file)
                file.close()

                return json.dumps({
                    'status': True
                })
                
        return json.dumps({
            'status': False
        })


class AddScheduleFrom(TemplateContextView):
    def get_context(self, request, *args, **kwargs):
        return {
            'source': Admin.objects.get(username=request.session['user']['username']).station.id,
            'stations': Station.objects.all(),
            'current_datetime': datetime.today().strftime("%H:%M")
        }
    
    def get_template(self):
        return "add_schedule_form.html"
