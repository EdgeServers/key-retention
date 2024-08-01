from django.urls import path
from. import views


urlpatterns = [
    path('', views.welcome, name='home'),
    path('arrival/', views.arrival, name='arrival'),
    path('departure/', views.departure, name='departure'),
    path('active_drivers/', views.active_drivers, name='active_drivers'),
    path('get_key_hanger_number/', views.get_key_hanger_number, name='get_key_hanger_number'),
    
]
