from django.urls import path
from . import views
 

urlpatterns = [
    #vehicle urls
    path('add_vehicle', views.add_vehicle, name='add_vehicle'),
    path('update_vehicle/<str:pk>', views.update_vehicle, name='update_vehicle'),
    path('remove_vehicle/<str:pk>', views.remove_vehicle, name='remove_vehicle'),
    path('view_vehicle/<str:pk>', views.view_vehicle, name='view_vehicle'),
    path('list_vehicles', views.list_vehicles, name='list_vehicles'),
    #--ends

    #driver urls
    path('add_driver', views.add_driver, name='add_driver'),
    path('update_driver/<str:pk>', views.update_driver, name='update_driver'),
    path('remove_driver/<str:pk>', views.remove_driver, name='remove_driver'),
    path('view_driver/<str:pk>', views.view_driver, name='view_driver'),
    path('list_drivers', views.list_drivers, name='list_drivers'),
    #--ends

    #Customer urls
    path('add_customer', views.add_customer, name='add_customer'),
    path('update_customer/<str:pk>', views.update_customer, name='update_customer'),
    path('remove_customer/<str:pk>', views.remove_customer, name='remove_customer'),
    path('view_customer/<str:pk>', views.view_customer, name='view_customer'),
    path('list_customers', views.list_customers, name='list_customers'),
    #--ends

]