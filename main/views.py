
from my_modules.base_views import TemplateContextView, NoTemplateView
from main.models import Station
from django.shortcuts import render,redirect

class HomePage(TemplateContextView):
    def get_template(self):
        return 'home_page.html'

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



