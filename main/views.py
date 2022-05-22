
from my_modules.base_views import TemplateContextView, NoTemplateView
from main.models import Station,Train,Car,Seat
from django.shortcuts import render,redirect

class Home(TemplateContextView):
    def get_template(self):
        return 'home_page.html'

class AddStationPage(TemplateContextView):
    def get_template(self):
        return 'add_station.html'

def add_station(request):
        if request.method == 'POST':
            st_name=request.POST.get('station_name')
            st_location=request.POST.get('station_location')
            st_description=request.POST.get('station_description')
            station = Station.objects.create(
                name=st_name,location=st_location,description=st_description
            )
        return redirect('main:add_station_page')


def add_station_page(request):
    return render(request, 'add_station.html')

def add_train_page(request):
    print('in add_train_page')
    context={}
    context['stations']=Station.objects.all()
    return render(request,'add_train.html',context)

def add_train(request):
    print('in add_train')
    f_berthNOS = 6*4
    f_seatNOS = 14*4
    s_chairNOS = 14*4
    shovanNOS = 16*4
    if request.method == 'POST':
        fr = request.POST.get('from')
        to = request.POST.get('to')
        f_berth = request.POST.get('f_berth')
        f_seat = request.POST.get('f_seat')
        s_chair = request.POST.get('s_chair')
        shovan = request.POST.get('shovan_fare')
        f_berth_fare = request.POST.get('f_berth_fare')
        f_seat_fare = request.POST.get('f_seat_fare')
        s_chair_fare = request.POST.get('s_chair_fare')
        shovan_fare = request.POST.get('shovan_fare')
        dept_time = request.POST.get('dept_time')

        #adding train
        source_station=Station.objects.filter(id=fr)[0]
        des_station=Station.objects.filter(id=to)[0]
        print(source_station)
        print(des_station)
        print(dept_time)
        print(f'dept is type {type(dept_time)}')

        # new_train = Train.objects.create(
        #     source=source_station,destination=des_station
        # )
    return redirect('main:add_train_page')



