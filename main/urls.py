from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("add_station_page", views.add_station_page, name="add_station_page"),
    path("add_station", views.add_station, name="add_station"),
    path("add_train_page",views.add_train_page, name = "add_train_page"),
    path("add_train",views.add_train, name = "add_train"),
]