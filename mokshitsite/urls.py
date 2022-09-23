from django.urls import path
from mokshitsite import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name ='services'),
    path('contact_us/', views.contact, name ='contact_us' ),
    path('career/',views.carrer, name ='career'),
    
]

