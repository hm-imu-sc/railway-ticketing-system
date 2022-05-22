from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.HomePage.as_view(), name="home_page"),
    path("passenger_registration_page", views.PassengerRegistrationPage.as_view(), name="passenger_registration_page"),
    path("passenger_registration", views.PassengerRegistration.as_view(), name="passenger_registration"),
    path("login_page", views.LoginPage.as_view(logout_required=True), name="login_page"),
    path("login", views.Login.as_view(logout_required=True), name="login"),
    path("logout", views.Logout.as_view(), name="logout"),
    path("add_station", views.addStation, name="add_station"),
]