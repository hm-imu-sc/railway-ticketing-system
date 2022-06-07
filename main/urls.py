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
    path("passenger_registration_page", views.PassengerRegistrationPage.as_view(logout_required=True), name="passenger_registration_page"),
    path("passenger_registration", views.PassengerRegistration.as_view(logout_required=True), name="passenger_registration"),
    path("login_page", views.LoginPage.as_view(logout_required=True), name="login_page"),
    path("login", views.Login.as_view(logout_required=True), name="login"),
    path("logout", views.Logout.as_view(login_required=True), name="logout"),
    path("get_schedule/<str:date>/<str:source>/<str:destination>", views.GetSchedule.as_view(), name="get_schedule"),
    path("seat_selection_page/<str:train_id>", views.SeatSelectionPage.as_view(login_required=True), name="seat_selection_page"),
    path("get_seats/<int:train_id>/<int:car_type_id>/<str:number_of_seats>/", views.GetSeats.as_view(login_required=True), name="get_seats"),
    path("seat_purchase/<int:train_id>/<int:car_type_id>/<str:number_of_seats>/", views.SeatPurchase.as_view(login_required=True), name="seat_purchse"),
    path("my_trips_page/", views.MyTripsPage.as_view(login_required=True), name="my_trips_page"),
    path("get_ticket_page/<int:payment_id>/", views.GetTicketPage.as_view(login_required=True), name="get_ticket_page"),
    path("scheduler_page/", views.SchedulerPage.as_view(login_required=True, admin_required=True), name="scheduler_page"),
    path("day_schedule/", views.DaySchedule.as_view(login_required=True, admin_required=True), name="dey_schedule"),
    path("add_schedule_form/", views.AddScheduleFrom.as_view(login_required=True, admin_required=True), name="add_schedule_form"),
    path("delete_day_schedule/<int:id>/", views.DeleteDaySchedule.as_view(login_required=True, admin_required=True), name="delete_day_schedule"),
    path("edit_schedule_page",views.EditSchedulePage.as_view(login_required=True, admin_required=True),name="edit_schedule_page"),
    path("get_schedule_by_date/<str:source>/<str:date>",views.GetScheduleByDate.as_view(login_required=True, admin_required=True),name="get_schedule_by_date"),
    path("delete_train/<int:train_id>",views.DeleteTrainFromSchedule.as_view(login_required=True, admin_required=True),name="delete_train_from_schedule"),
    path("update_train_time/<int:train_id>/<str:time>",views.UpdateScheduleTime.as_view(login_required=True, admin_required=True),name="delete_train_from_schedule"),
    path("week_schedule_controls/", views.WeekScheduleControls.as_view(login_required=True, admin_required=True), name="week_schedule_controls"),
    path("revert_week_day/<int:index>/", views.RevertWeekDay.as_view(login_required=True, admin_required=True), name="revert_week_day"),
    path("get_week_day_schedule/<int:index>/", views.GetWeekDaySchedule.as_view(login_required=True, admin_required=True), name="get_week_day_schedule"),
    path("delete_week_day_schedule/<int:schedule_id>/<int:day_id>/", views.DeleteWeekDaySchedule.as_view(login_required=True, admin_required=True), name="delete_week_day_schedule"),
    path("add_week_day_schedule_form/<int:index>/", views.AddWeekDayScheduleFrom.as_view(login_required=True, admin_required=True), name="add_week_day_schedule_form"),
    path("add_week_day_schedule/<int:index>/", views.AddWeekDaySchedule.as_view(login_required=True, admin_required=True), name="add_week_day_schedule"),
    path("schedule_applier_controls/", views.ScheduleApplierControls.as_view(login_required=True, admin_required=True), name="schedule_applier_controls"),
    path("apply_schedule/", views.ApplySchedule.as_view(login_required=True, admin_required=True), name="apply_schedule")
]


    # path("add_station_page", views.add_station_page, name="add_station_page"),
    # path("add_station", views.add_station, name="add_station"),
    # path("add_train_page",views.add_train_page, name = "add_train_page"),
    # path("add_train",views.add_train, name = "add_train"),