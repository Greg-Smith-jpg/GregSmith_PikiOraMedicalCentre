from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'appointmentSystem/home.html')

def doctors(request):
    from .models import Doctor
    doctors = Doctor.objects.all()
    return render(request,
                  'appointmentSystem/doctors.html',
                  {'doctors': doctors}
    )

def doctor_slots(request, doctor_id):
    from .models import Doctor

    doctor = Doctor.objects.get(id=doctor_id)
    slots = doctor.appointment_slots.filter(is_available=True)

    return render(
        request,
        'appointmentSystem/doctor_slots.html',
        {
            'doctor': doctor,
            'slots': slots
        }
    )
@login_required
def book_appointment(request, slot_id):
    from .models import AppointmentSlot, Appointment

    slot = AppointmentSlot.objects.get(id=slot_id)

    if request.method == "POST":
        if not slot.is_available:
            return redirect("doctors")

        Appointment.objects.create(
            patient=request.user,
            appointment_slot=slot
        )

        slot.is_available = False
        slot.save()

        return redirect("my_appointments")

    return render(
        request,
        "appointmentSystem/book_appointment.html",
        {"slot": slot}
    )

@login_required
def my_appointments(request):
    from .models import Appointment
    appointments = Appointment.objects.filter(
        patient=request.user,
        status="Booked"
    )
    return render(
        request,
        'appointmentSystem/my_appointments.html',
        {'appointments': appointments}
    )

@login_required
def cancel_appointment(request, appointment_id):
    from .models import Appointment

    appointment = Appointment.objects.get(
        id=appointment_id,
        patient=request.user
    )

    if request.method == "POST":
        appointment.appointment_slot.is_available = True
        appointment.appointment_slot.save()

        appointment.status = "Cancelled"
        appointment.save()

        return redirect("my_appointments")

    return render(
        request,
        "appointmentSystem/cancel_appointment.html",
        {"appointment": appointment}
    )