from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.HomePage.as_view(), name="home_page"),
    path("admin_home_page/", views.AdminHomePage.as_view(login_required=True, admin_required=True), name="admin_home_page"),
    path("add_station_page", views.AddStationPage.as_view(login_required=True, admin_required=True), name="add_station_page"),
    path("add_station/<str:name>/<str:location>/<str:desc>", views.AddStation.as_view(login_required=True, admin_required=True), name="add_station"),
    path("add_train_page",views.AddTrainPage.as_view(login_required=True, admin_required=True), name = "add_train_page"),
    path("add_train",views.AddTrain.as_view(login_required=True, admin_required=True), name = "add_train"),
    path("passenger_registration_page", views.PassengerRegistrationPage.as_view(), name="passenger_registration_page"),
    path("passenger_registration", views.PassengerRegistration.as_view(), name="passenger_registration"),
    path("login_page", views.LoginPage.as_view(logout_required=True), name="login_page"),
    path("login", views.Login.as_view(logout_required=True), name="login"),
    path("logout", views.Logout.as_view(), name="logout"),
    path("get_schedule/<str:date>/<str:source>/<str:destination>", views.GetSchedule.as_view(), name="get_schedule"),
    path("seat_selection_page/<str:train_id>", views.SeatSelectionPage.as_view(login_required=True), name="seat_selection_page"),
]





    # path("add_station_page", views.add_station_page, name="add_station_page"),
    # path("add_station", views.add_station, name="add_station"),
    # path("add_train_page",views.add_train_page, name = "add_train_page"),
    # path("add_train",views.add_train, name = "add_train"),