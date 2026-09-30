from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('doctors/', views.doctors, name='doctors'),
    path('doctors/<int:doctor_id>/', views.doctor_slots, name='doctor_slots'),
    path("appointments/book/<int:slot_id>", views.book_appointment, name="book_appointment")
]