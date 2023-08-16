from django.urls import path
from . import views
 

urlpatterns = [
    path('add_vehicle', views.add_vehicle, name='add_vehicle'),

]