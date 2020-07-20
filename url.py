from django.urls import path
from . import views

urlpatterns = [
    path('shuttlephoto', views.shuttle_photo),
    path('shuttlestop', views.stop_detail),
    path('shuttle', views.shuttle),
    path('food', views.food),
    path('lib', views.library),
    path('campus', views.update_campus)
]