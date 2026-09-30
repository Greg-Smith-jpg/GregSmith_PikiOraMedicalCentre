from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class AppointmentSlot(models.Model):
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='appointment_slots'
    )
    date = models.DateField()
    time = models.TimeField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.doctor.name} - {self.date} {self.time}'


class Appointment(models.Model):
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    appointment_slot = models.ForeignKey(
        AppointmentSlot,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Booked')

    def __str__(self):
        return f'{self.patient.name} - {self.appointment_slot}'
