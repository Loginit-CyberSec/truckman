from django.urls import path
from . import views
 

urlpatterns = [
    #organization urls
    path('register', views.register_user, name='register'),
    path('login', views.login_user, name='login'), 
    path('logout', views.logout_user, name='logout'), 

    #role urls
    path('add_role', views.add_role, name='add_role'),
    path('list_roles', views.list_roles, name='list_roles'), 
    path('view_role/<str:pk>', views.view_role, name='view_role'), 
    path('update_role/<str:pk>', views.update_role, name='update_role'), 
    path('remove_role/<str:pk>', views.remove_role, name='remove_role'), 

    #staff urls
    path('add_staff', views.add_staff, name='add_staff'),
    path('list_staffs', views.list_staffs, name='list_staffs'), 
    path('view_staff/<str:pk>', views.view_staff, name='view_staff'), 
    path('update_staff/<str:pk>', views.update_staff, name='update_staff'), 
    path('remove_staff/<str:pk>', views.remove_staff, name='remove_staff'), 

    #user urls
    path('user_profile/<str:pk>', views.user_profile, name='user_profile'), 
    path('update_user_profile/<str:pk>', views.update_user_profile, name='update_user_profile'), 
    path('settings', views.global_settings, name='global_settings'), 
]