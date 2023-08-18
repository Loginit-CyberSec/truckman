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

    #shipper urls
    path('add_shipper', views.add_shipper, name='add_shipper'),
    path('update_shipper/<str:pk>', views.update_shipper, name='update_shipper'),
    path('remove_shipper/<str:pk>', views.remove_shipper, name='remove_shipper'),
    path('view_shipper/<str:pk>', views.view_shipper, name='view_shipper'),
    path('list_shippers', views.list_shippers, name='list_shippers'),
    #--ends

    #Consignee urls
    path('add_consignee', views.add_consignee, name='add_consignee'),
    path('update_consignee/<str:pk>', views.update_consignee, name='update_consignee'),
    path('remove_consignee/<str:pk>', views.remove_consignee, name='remove_consignee'),
    path('view_consignee/<str:pk>', views.view_consignee, name='view_consignee'),
    path('list_consignees', views.list_consignees, name='list_consignees'),
    #--ends

    #load urls
    path('add_load', views.add_load, name='add_load'),
    path('update_load/<str:pk>', views.update_load, name='update_load'),
    path('remove_load/<str:pk>', views.remove_load, name='remove_load'),
    path('view_load/<str:pk>', views.view_load, name='view_load'),
    path('list_loads', views.list_loads, name='list_loads'),
    #--ends

    #trip urls
    path('add_trip', views.add_trip, name='add_trip'),
    path('update_trip/<str:pk>', views.update_trip, name='update_trip'),
    path('remove_trip/<str:pk>', views.remove_trip, name='remove_trip'),
    path('view_trip/<str:pk>', views.view_trip, name='view_trip'),
    path('list_trips', views.list_trips, name='list_trips'),
    #--ends

]