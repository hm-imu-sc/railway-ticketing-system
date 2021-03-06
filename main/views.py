
from my_modules.utils import get_week_schedule_format
from my_modules.base_views import APIOnlyView, TemplateContextView, NoTemplateView, ActionOnlyView
from main.models import Station, Passenger, Admin, Train, Car, Seat, Payment
from django.utils.dateparse import parse_datetime
from django.shortcuts import render,redirect
from datetime import datetime, timedelta
from hashlib import sha256
import zoneinfo
import json
from django.http import HttpResponse
import random

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
            'stations': stations,
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

        car_types = [
            "First Class Berth",
            "First Class Seat",
            "Shovan Chair",
            "Shovan",
        ]

        c = 0

        distinct_cars = []

        all_cars = list(train.car_set.all())

        for car in all_cars:
            if car.car_type == car_types[c]:
                distinct_cars.append({
                    "id": c,
                    "name": car.car_type,
                    "fare": int(car.fare),
                })
                c+=1

                if c == 4:
                    break

        print(distinct_cars)

        return {
            'train_id': train_id,
            'cars': distinct_cars,
        }

    def get_template(self):
        return 'seat_selection_page.html'


class GetSchedule(TemplateContextView):

    def get_context(self, request, *args, **kwargs):
        date = datetime(*[int(i) for i in kwargs['date'].split("-")[::-1]])
        source = Station.objects.get(id=int(kwargs['source']))
        destination = Station.objects.get(id=int(kwargs['destination']))

        train_schedules = []

        for train in Train.objects.all():

            if datetime(train.departure.year, train.departure.month, train.departure.day) == date and train.source == source and train.destination == destination:
                
                seats = 0
                booked = 0

                for car in train.car_set.all():
                    seats += car.number_of_seats
                    booked += len(car.seat_set.all())

                booked_percent = 0 if booked == 0 else int(seats/booked)*100
                booked_class = ''

                if seats == booked:
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
                    'source': source.location,
                    'destination': destination.location,
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


class GetSeats(APIOnlyView):
    def get_return(self, request, *args, **kwargs):
        
        train = Train.objects.get(id=kwargs["train_id"])
        car_type_id = kwargs["car_type_id"]
        number_of_seats = int(kwargs["number_of_seats"])

        car_types = [
            "First Class Berth",
            "First Class Seat",
            "Shovan Chair",
            "Shovan",
        ]

        total_seats = 0
        seats = 0
        fare = 0
        status = True
        message = "All seats are available !!!"

        for car in train.car_set.filter(car_type=car_types[car_type_id]):
            fare = car.fare
            total_seats += car.number_of_seats
            seats += len(car.seat_set.all())

        # print(f"{train.id} | {total_seats} | {seats}")

        if total_seats-seats < number_of_seats:
            status = False
            message = f"Sorry! only {total_seats-seats} seats available in this car !!!"

        return {
            "status": status,
            "seats": seats,
            "fare": int(fare),
            "car": car_type_id,
            "message": message
        }


class SeatPurchase(ActionOnlyView):
    def act(self, request, *args, **kwargs):
        
        car_types = [
            "First Class Berth",
            "First Class Seat",
            "Shovan Chair",
            "Shovan",
        ]

        train = Train.objects.get(id=kwargs["train_id"])
        car_type_id = kwargs["car_type_id"]
        number_of_seats = int(kwargs["number_of_seats"])
        passenger = Passenger.objects.get(username=request.session["user"]["username"])
        
        seats = 0

        for car in train.car_set.filter(car_type=car_types[car_type_id]):
            seats += len(car.seat_set.all())

        payment = Payment.objects.create(
            passenger=passenger,
            amount=train.car_set.filter(car_type=car_types[car_type_id])[0].fare*number_of_seats,
            date=datetime(train.departure.year, train.departure.month, train.departure.day),
            seat_serial=seats
        )

        for car in train.car_set.filter(car_type=car_types[car_type_id]):

            available = car.number_of_seats - len(car.seat_set.all())

            if available > 0 and number_of_seats > 0:

                purchasing_now = min(available, number_of_seats)

                for i in range(purchasing_now):
                    Seat.objects.create(
                        car=car,
                        bought_by=passenger,
                        is_sold=True,
                        payment=payment
                    )

                number_of_seats -= purchasing_now

        return json.dumps({
            "status": True,
            "message": "Ticket purchase and payment successfull !!!\nYou can download your tickets from \"My Trips\""
        })


class MyTripsPage(TemplateContextView):
    def get_context(self, request, *args, **kwargs):
        
        passenger = Passenger.objects.get(username=request.session["user"]["username"])
        
        upcoming_trips = []
        previous_trips = []

        for payment in Payment.objects.filter(passenger=passenger):
            number_of_seats = len(payment.seat_set.all())
            train = payment.seat_set.first().car.train
            car_type = payment.seat_set.first().car.car_type

            seat_prefix = "".join([word[0] for word in car_type.split()])
            seat_string = ", ".join(f"{seat_prefix}-{seat}" for seat in range(payment.seat_serial + number_of_seats)[payment.seat_serial:])

            trip = {
                "source": train.source.location,
                "destination": train.destination.location,
                "departure": train.departure.strftime("%d-%m-%Y %I:%M %p"),
                "seat_string": seat_string,
                "payment_amount": payment.amount,
                "payment_id": payment.id,
            }

            departure = datetime(train.departure.year, train.departure.month, train.departure.day, train.departure.hour, train.departure.minute)

            if departure < datetime.now():
                previous_trips.append(trip)
            else:
                upcoming_trips.append(trip)

        # print(upcoming_trips)
        # print(previous_trips)

        return {
            'upcoming_trips': upcoming_trips,
            'previous_trips': previous_trips,
            'nav': {
                "my_trips_page": "active"
            }
        }

    def get_template(self):
        return "my_trips_page.html"


class GetTicketPage(TemplateContextView):
    def get_context(self, request, *args, **kwargs):
        
        passenger = Passenger.objects.get(username=request.session["user"]["username"])
        payment = Payment.objects.get(id=kwargs["payment_id"])
        car_type = payment.seat_set.first().car.car_type
        train = payment.seat_set.first().car.train

        number_of_seats = len(payment.seat_set.all())
        seat_prefix = "".join([word[0] for word in car_type.split()])
        seat_string = ", ".join(f"{seat_prefix}-{seat}" for seat in range(payment.seat_serial + number_of_seats)[payment.seat_serial:])

        return {
            "passenger_name": passenger.name,
            "seat_string": seat_string,
            "payment_amount": payment.amount,
            "from": {
                "location": train.source.location,
                "date": train.departure.strftime("%d-%m-%Y"),
                "time": train.departure.strftime("%I:%M %p")
            },
            "to": {
                "location": train.destination.location,
                "date": (train.departure+timedelta(hours=random.choice([6,7,8,9,10,12]))).strftime("%d-%m-%Y"),
                "time": (train.departure+timedelta(hours=random.choice([6,7,8,9,10,12]))).strftime("%I:%M %p")
            }
        }

    def get_template(self):
        return "get_ticket_page.html"


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
        return 'main:login_page'


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
                request.session.set_expiry(3600*24)

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

            # adding train
            source_station = Station.objects.filter(id=fr)[0]
            des_station = Station.objects.filter(id=to)[0]
            # print(dept_time)
            dept_time = dept_time.replace('T', ' ')
            dept_time = dept_time.replace('-', ' ')
            dept_time = dept_time.replace(':', ' ')
            time=dept_time.split(" ")
            # print(time)
            dept_time = datetime(int(time[0]),int(time[1]),int(time[2]),int(time[3]),int(time[4]))
            # print(dept_time)
            # print(f'dept_time is type {type(dept_time)}')
            opening_date = dept_time - timedelta(days=14)

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


class EditSchedulePage(TemplateContextView):
    def get_context(self, request, *args, **kwargs):
        context = {}
        context['stations'] = Station.objects.all()
        context["date"] = datetime.now().strftime("%Y-%m-%d")
        return context
    def get_template(self):
        return 'edit_schedule_page.html'


class GetScheduleByDate(TemplateContextView):
    def get_context(self, request, *args, **kwargs):
        context = {}
        date = kwargs['date']
        source = kwargs['source']
        #print(f"getting schedule for source: {source} and date: {date}")
        year = date.split('-')[0]
        month = date.split('-')[1]
        day = date.split('-')[2]
        #print(f"{year} {month} {day}")
        trains = Train.objects.filter(departure__year=year,departure__month=month,departure__day=day,source=source)
        modded_trains = []
        for train in trains:
            modded_trains.append((train,train.departure.strftime("%H:%M")))
        #print(len(trains))
        context['trains']=modded_trains

        return context
    def get_template(self):
        return 'edit_schedule_table.html'


class DeleteTrainFromSchedule(ActionOnlyView):
    def act(self, request, *args, **kwargs):
        train_id=kwargs['train_id']
        Train.objects.get(id=train_id).delete()


class UpdateScheduleTime(ActionOnlyView):
    def act(self, request, *args, **kwargs):
        train_id = kwargs['train_id']
        times = kwargs['time'].split(":")
        train=Train.objects.get(id=train_id)
        train.departure=train.departure.replace(hour=int(times[0]),minute=int(times[1]))
        train.save()


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
        
        try:
            file = open(f'json/default_day_schedule_{station_id}.json', 'r')
            day_schedule = json.load(file)
            file.close()
        except FileNotFoundError:
            day_schedule = []

        next_id = 0

        for schedule in day_schedule:
            next_id = max(next_id, schedule['id'])

        if request.method == "GET":
            context = {
                "schedules": [],
                "add_button_required": True,
            }

            for schedule in day_schedule:

                schedule['source'] = Station.objects.get(id=int(schedule['source'])).location
                schedule['destination'] = Station.objects.get(id=int(schedule['destination'])).location
                schedule['time'] = datetime(2022, 1, 1, *[int(t) for t in schedule['time'].split(":")]).strftime("%I:%M %p")
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
                        'type': 'First Class Berth',
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
            schedule['time'] = datetime(2022, 1, 1, *[int(t) for t in schedule['time'].split(":")]).strftime("%I:%M %p")

            return {
                "schedules": [schedule],
                "add_button_required": False,
            }

    def get_template(self):
        return "schedule.html"


class DeleteDaySchedule(ActionOnlyView):
    def act(self, request, *args, **kwargs):
        to_delete = kwargs['id']
        
        station_id = Admin.objects.get(username=request.session['user']['username']).station.id

        # print(f'PATH: json/default_day_schedule_{station_id}.json')

        try:
            file = open(f'json/default_day_schedule_{station_id}.json', 'r')
            all_schedules = json.load(file)
            file.close()
        except FileNotFoundError:
            all_schedules = []

        for i in range(len(all_schedules)):
            if all_schedules[i]['id'] == to_delete:
                all_schedules.remove(all_schedules[i])        

                file = open(f'json/default_day_schedule_{station_id}.json', 'w')
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


class WeekScheduleControls(TemplateContextView):
    def get_context(self, request, *args, **kwargs):
        
        station_id = Admin.objects.get(username=request.session['user']['username']).station.id
        today = datetime.today().strftime('%A')

        try:
            file =  open(f'json/default_week_schedule_{station_id}.json', 'r')
            week_shedule = json.load(file)
            file.close()
        except FileNotFoundError:
            week_shedule = get_week_schedule_format()

        for i in range(len(week_shedule)):

            week_shedule[i]["index"] = i

            if week_shedule[i]["day"] == today:
                week_shedule[i]["active"] = "active"
                today_schedule = self.process_schedule(week_shedule[i]["schedule"])
                revert = i
            else:
                week_shedule[i]["active"] = ""
        
        return {
            "week_days": week_shedule,
            "today_schedule": today_schedule,
            "revert": revert
        }

    def get_template(self):
        return "week_schedule_controls.html"

    def process_schedule(self, all_schedule):
        for i in range(len(all_schedule)):
            all_schedule[i]["source"] = Station.objects.get(id=int(all_schedule[i]["source"])).location
            all_schedule[i]["destination"] = Station.objects.get(id=int(all_schedule[i]["destination"])).location
            all_schedule[i]["time"] = datetime(2022, 1, 1, *[int(t) for t in all_schedule[i]["time"].split(":")]).strftime("%I:%M %p")

        return all_schedule


class RevertWeekDay(TemplateContextView):
    def get_context(self, request, *args, **kwargs):
        index = kwargs["index"]
        
        station_id = Admin.objects.get(username=request.session['user']['username']).station.id
        filename_default_day = f'json/default_day_schedule_{station_id}.json'
        filename_default_week = f'json/default_week_schedule_{station_id}.json'

        try:
            file = open(filename_default_day, 'r')
            all_schedules = json.load(file)
            file.close()
        except FileNotFoundError:
            all_schedules = []

        try:
            file =  open(filename_default_week, 'r')
            week_shedule = json.load(file)
            file.close()
        except FileNotFoundError:
            week_shedule = get_week_schedule_format()

        week_shedule[index]["schedule"] = all_schedules

        file = open(filename_default_week, 'w')
        json.dump(week_shedule, file)
        file.close()

        return {
            "schedule_id": index,
            "schedules": self.process_schedule(all_schedules),
            "add_button_required": True,
            "week": True,
        }

    def get_template(self):
        return "schedule.html"

    def process_schedule(self, all_schedule):
        for i in range(len(all_schedule)):
            all_schedule[i]["source"] = Station.objects.get(id=int(all_schedule[i]["source"])).location
            all_schedule[i]["destination"] = Station.objects.get(id=int(all_schedule[i]["destination"])).location
            all_schedule[i]["time"] = datetime(2022, 1, 1, *[int(t) for t in all_schedule[i]["time"].split(":")]).strftime("%I:%M %p")

        return all_schedule


class GetWeekDaySchedule(TemplateContextView):
    def get_context(self, request, *args, **kwargs):
        index = kwargs["index"]
        
        station_id = Admin.objects.get(username=request.session['user']['username']).station.id
        filename = f'json/default_week_schedule_{station_id}.json'

        try:
            file =  open(filename, 'r')
            week_shedule = json.load(file)
            file.close()
        except FileNotFoundError:
            week_shedule = get_week_schedule_format()

        return {
            "schedules": self.process_schedule(week_shedule[index]["schedule"]),
            "schedule_id": index,
            "add_button_required": True,
            "week": True,
        }
    
    def get_template(self):
        return "schedule.html"

    def process_schedule(self, all_schedule):
        for i in range(len(all_schedule)):
            all_schedule[i]["source"] = Station.objects.get(id=int(all_schedule[i]["source"])).location
            all_schedule[i]["destination"] = Station.objects.get(id=int(all_schedule[i]["destination"])).location
            all_schedule[i]["time"] = datetime(2022, 1, 1, *[int(t) for t in all_schedule[i]["time"].split(":")]).strftime("%I:%M %p")

        return all_schedule


class DeleteWeekDaySchedule(ActionOnlyView):
    def act(self, request, *args, **kwargs):
        station_id = Admin.objects.get(username=request.session['user']['username']).station.id
        filename = f'json/default_week_schedule_{station_id}.json'

        day_id = kwargs["day_id"]
        schedule_id = kwargs["schedule_id"]

        file = open(filename, 'r')
        week_schedules = json.load(file)
        file.close()

        for schedule in week_schedules[schedule_id]["schedule"]:
            if schedule["id"] == day_id:
                week_schedules[schedule_id]["schedule"].remove(schedule)

                file = open(filename, 'w')
                json.dump(week_schedules, file)
                file.close()

                return json.dumps({
                    "status": True
                })

        return {
            "status": False
        }
        

class AddWeekDayScheduleFrom(TemplateContextView):
    def get_context(self, request, *args, **kwargs):
        return {
            'index': kwargs['index'],
            'source': Admin.objects.get(username=request.session['user']['username']).station.id,
            'stations': Station.objects.all(),
            'current_datetime': datetime.today().strftime("%H:%M")
        }

    def get_template(self):
        return "add_week_day_schedule_form.html"


class AddWeekDaySchedule(TemplateContextView):
    def get_context(self, request, *args, **kwargs):

        index = kwargs["index"]
        station_id = Admin.objects.get(username=request.session['user']['username']).station.id
        filename = f'json/default_week_schedule_{station_id}.json'

        try:
            file = open(filename, 'r')
            week_schedule = json.load(file)
            file.close()
        except FileNotFoundError:
            week_schedule = get_week_schedule_format()

        next_id = 0

        for schedule in week_schedule[index]["schedule"]:
            next_id = max(next_id, schedule['id'])

        schedule = {
            'id': next_id+1,
            'source': request.POST.get('source'),
            'destination': request.POST.get('dest'),
            'time': request.POST.get('dept'),
            'cars': [
                {
                    'type': 'First Class Berth',
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

        week_schedule[index]["schedule"].append(schedule)

        file = open(filename, 'w')
        json.dump(week_schedule, file)
        file.close()

        schedule['source'] = Station.objects.get(id=int(schedule['source'])).location
        schedule['destination'] = Station.objects.get(id=int(schedule['destination'])).location
        schedule['time'] = datetime(2022, 1, 1, *[int(t) for t in schedule['time'].split(":")]).strftime("%I:%M %p")

        return {
            "schedule_id": index,
            "schedules": [schedule],
            "add_button_required": False,
            "week": True,
        }

    def get_template(self):
        return "schedule.html"


class ScheduleApplierControls(TemplateContextView):
    def get_context(self, request, *args, **kwargs):
        return {
            "today": datetime.today().strftime("%Y-%m-%d")
        }
    
    def get_template(self):
        return "schedule_applier_controls.html"


class ApplySchedule(ActionOnlyView):
    def act(self, request, *args, **kwargs):

        # print(f"{request.GET.get('from')} -> {request.GET.get('to')}")
        # return

        _from = datetime(*[int(i) for i in request.GET.get("from").split("-")])
        _to = datetime(*[int(i) for i in request.GET.get("to").split("-")])

        station_id = Admin.objects.get(username=request.session['user']['username']).station.id
        filename = f'json/default_week_schedule_{station_id}.json'

        idx = {
            "Fri": 0,
            "Sat": 1,
            "Sun": 2,
            "Mon": 3,
            "Tue": 4,
            "Wed": 5,
            "Thu": 6,
        }

        try:
            file = open(filename, 'r')
            week_schedule = json.load(file)
            file.close()
        except FileNotFoundError:
            week_schedule = get_week_schedule_format()

        s = 0

        while _from <= _to:
            day = datetime(_from.year, _from.month, _from.day).strftime("%a")
            
            for schedule in week_schedule[idx[day]]["schedule"]:
                
                date = datetime(_from.year, _from.month, _from.day, *[int(i) for i in schedule["time"].split(":")])
                
                # print(f"{date} | {date.strftime('%Y-%m-%d %I:%M %p')} | {schedule['time']}")

                train = Train.objects.create(
                    source=Station.objects.get(id=int(schedule["source"])),
                    destination=Station.objects.get(id=int(schedule["destination"])),
                    departure=date
                )

                for car_info in schedule["cars"]:

                    for c in range(car_info["number_of_cars"]):

                        car = Car.objects.create(
                            train=train,
                            car_type=car_info["type"],
                            fare=car_info["fare"],
                            number_of_seats=car_info["seats_per_car"]
                        )

                        # for i in range(car.number_of_seats):
                            # print(f"creating seat: {s}")
                            # s += 1
                            # Seat.objects.create(car=car)
                    

            _from += timedelta(days=1)

        # print(request.GET)

        return json.dumps({
            "status": True,
            "message": "Schedules applied successfully !!!",
        })

