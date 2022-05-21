from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.HomePage.as_view(), name="home_page"),
    path("passenger_registration_page", views.PassengerRegistrationPage.as_view(), name="passenger_registration_page"),
    path("add_station", views.addStation, name="add_station"),
]