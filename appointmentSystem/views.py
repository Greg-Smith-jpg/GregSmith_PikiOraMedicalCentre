from django.shortcuts import render, redirect

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

def book_appointment(request, slot_id):
    from .models import AppointmentSlot, Appointment

    slot = AppointmentSlot.objects.get(id=slot_id)

    if request.method == "POST":
        Appointment.objects.create(
            patient=request.user,
            appointment_slot=slot
        )

        slot.is_available = False
        slot.save()

        return redirect("home")

    return render(
        request,
        "appointmentSystem/book_appointment.html",
        {"slot": slot}
    )