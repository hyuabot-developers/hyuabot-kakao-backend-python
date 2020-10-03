from django.urls import path
from kakao_i_hanyang.views import *

urlpatterns = [
    path('shuttle', get_shuttle_departure_info),
    path('shuttle/stop', get_shuttle_stop_info),
    path('food', get_food_menu),
    path('library/seats', get_reading_room_seat_info),
    path('update/campus', update_campus)
]