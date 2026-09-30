
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from .forms import DoctorForm, AppointmentBookingForm, AppointmentReasonForm


# Create your views here.

def home(request):
    return render(request, 'appointmentSystem/home.html')


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Your account has been created successfully. You can now log in."
            )

            return redirect("login")

    else:
        form = UserCreationForm()

    return render(
        request,
        "registration/register.html",
        {
            "form": form
        }
    )


def doctors(request):
    from .models import Doctor

    doctors = Doctor.objects.all()

    return render(
        request,
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

    if not slot.is_available:
        messages.error(
            request,
            "This appointment slot is no longer available."
        )
        return redirect("doctors")

    if request.method == "POST":
        form = AppointmentBookingForm(request.POST)

        if form.is_valid():
            Appointment.objects.create(
                patient=request.user,
                appointment_slot=slot,
                reason=form.cleaned_data["reason"]
            )

            slot.is_available = False
            slot.save()

            messages.success(
                request,
                "Your appointment has been booked successfully."
            )

            return redirect("my_appointments")

    else:
        form = AppointmentBookingForm()

    return render(
        request,
        "appointmentSystem/book_appointment.html",
        {
            "slot": slot,
            "form": form
        }
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


@login_required
def edit_reason(request, appointment_id):
    from .models import Appointment

    appointment = Appointment.objects.get(
        id=appointment_id,
        patient=request.user
    )

    if request.method == "POST":

        form = AppointmentReasonForm(request.POST)

        if form.is_valid():
            appointment.reason = form.cleaned_data["reason"]
            appointment.save()

            messages.success(
                request,
                "Appointment reason updated successfully."
            )

        else:
            messages.error(
                request,
                "The appointment reason could not be updated. "
                "Please check that it is valid."
            )

    return redirect("my_appointments")


def is_admin(user):
    return user.is_staff


@user_passes_test(is_admin)
def admin_dashboard(request):
    from .models import Doctor, Appointment

    doctors = Doctor.objects.all()

    for doctor in doctors:
        doctor.has_booked_appointments = Appointment.objects.filter(
            appointment_slot__doctor=doctor,
            status="Booked"
        ).exists()

    return render(
        request,
        "appointmentSystem/admin_dashboard.html",
        {"doctors": doctors}
    )


@user_passes_test(is_admin)
def add_doctor(request):

    if request.method == "POST":
        form = DoctorForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Doctor added successfully."
            )

            return redirect("admin_dashboard")

    else:
        form = DoctorForm()

    return render(
        request,
        "appointmentSystem/add_doctor.html",
        {"form": form}
    )


@user_passes_test(is_admin)
def edit_doctor(request, doctor_id):
    from .models import Doctor

    doctor = Doctor.objects.get(id=doctor_id)

    if request.method == "POST":
        form = DoctorForm(
            request.POST,
            instance=doctor
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Doctor updated successfully."
            )

            return redirect("admin_dashboard")

    else:
        form = DoctorForm(instance=doctor)

    return render(
        request,
        "appointmentSystem/edit_doctor.html",
        {
            "doctor": doctor,
            "form": form
        }
    )


@login_required
@user_passes_test(is_admin)
def delete_doctor(request, doctor_id):
    from .models import Doctor, Appointment

    doctor = Doctor.objects.get(id=doctor_id)

    if request.method == "POST":

        booked_appointments = Appointment.objects.filter(
            appointment_slot__doctor=doctor,
            status="Booked"
        ).exists()

        if booked_appointments:
            messages.error(
                request,
                f"Cannot delete Dr. {doctor.name} because they have booked appointments."
            )

            return redirect("admin_dashboard")

        doctor_name = doctor.name

        doctor.delete()

        messages.success(
            request,
            f"Dr. {doctor_name} and all associated appointments and slots were deleted."
        )

        return redirect("admin_dashboard")

    return redirect("admin_dashboard")


@user_passes_test(is_admin)
def manage_slots(request, doctor_id):
    from .models import Doctor

    doctor = Doctor.objects.get(id=doctor_id)

    slots = doctor.appointment_slots.order_by(
        "date",
        "time"
    )

    return render(
        request,
        "appointmentSystem/manage_slots.html",
        {
            "doctor": doctor,
            "slots": slots
        }
    )


@user_passes_test(is_admin)
def add_slot(request, doctor_id):
    from .models import Doctor, AppointmentSlot

    doctor = Doctor.objects.get(id=doctor_id)

    if request.method == "POST":

        AppointmentSlot.objects.create(
            doctor=doctor,
            date=request.POST["date"],
            time=request.POST["time"]
        )

        messages.success(
            request,
            f"Appointment slot added for Dr. {doctor.name}."
        )

        return redirect(
            "manage_slots",
            doctor_id=doctor.id
        )

    return render(
        request,
        "appointmentSystem/add_slot.html",
        {
            "doctor": doctor
        }
    )


@user_passes_test(is_admin)
def edit_slot(request, slot_id):
    from .models import AppointmentSlot

    slot = AppointmentSlot.objects.get(id=slot_id)

    if request.method == "POST":

        slot.date = request.POST["date"]
        slot.time = request.POST["time"]
        slot.save()

        messages.success(
            request,
            "Appointment slot updated successfully."
        )

        return redirect(
            "manage_slots",
            doctor_id=slot.doctor.id
        )

    return render(
        request,
        "appointmentSystem/edit_slot.html",
        {
            "slot": slot
        }
    )


@user_passes_test(is_admin)
def delete_slot(request, slot_id):
    from .models import AppointmentSlot, Appointment

    slot = AppointmentSlot.objects.get(id=slot_id)

    doctor_id = slot.doctor.id

    booked = Appointment.objects.filter(
        appointment_slot=slot,
        status="Booked"
    ).exists()

    if booked:
        messages.error(
            request,
            "This appointment slot cannot be deleted because it currently has a booked appointment."
        )

        return redirect(
            "manage_slots",
            doctor_id=doctor_id
        )

    slot.delete()

    messages.success(
        request,
        "Appointment slot deleted successfully."
    )

    return redirect(
        "manage_slots",
        doctor_id=doctor_id
    )


@user_passes_test(is_admin)
def admin_appointments(request):
    from .models import Appointment

    appointments = Appointment.objects.select_related(
        "patient",
        "appointment_slot__doctor"
    ).order_by(
        "appointment_slot__date",
        "appointment_slot__time"
    )

    return render(
        request,
        "appointmentSystem/admin_appointments.html",
        {
            "appointments": appointments
        }
    )


@user_passes_test(is_admin)
def admin_edit_appointment(request, appointment_id):
    from .models import Appointment

    appointment = Appointment.objects.get(
        id=appointment_id
    )

    if request.method == "POST":

        form = AppointmentReasonForm(request.POST)

        if form.is_valid():
            appointment.reason = form.cleaned_data["reason"]
            appointment.save()

            messages.success(
                request,
                "Appointment updated successfully."
            )

            return redirect("admin_appointments")

    else:
        form = AppointmentReasonForm(
            initial={
                "reason": appointment.reason
            }
        )

    return render(
        request,
        "appointmentSystem/admin_edit_appointment.html",
        {
            "appointment": appointment,
            "form": form
        }
    )


@user_passes_test(is_admin)
def admin_cancel_appointment(request, appointment_id):
    from .models import Appointment

    appointment = Appointment.objects.get(
        id=appointment_id
    )

    if request.method == "POST":

        appointment.appointment_slot.is_available = True
        appointment.appointment_slot.save()

        appointment.status = "Cancelled"
        appointment.save()

        messages.success(
            request,
            "Appointment cancelled successfully."
        )

        return redirect("admin_appointments")

    return redirect("admin_appointments")


@user_passes_test(is_admin)
def manage_patients(request):
    from django.contrib.auth.models import User

    patients = User.objects.filter(
        is_staff=False
    ).order_by("username")

    return render(
        request,
        "appointmentSystem/manage_patients.html",
        {
            "patients": patients
        }
    )


@user_passes_test(is_admin)
def toggle_patient_status(request, patient_id):
    from django.contrib.auth.models import User

    patient = User.objects.get(
        id=patient_id,
        is_staff=False
    )

    if request.method == "POST":

        patient.is_active = not patient.is_active
        patient.save()

        if patient.is_active:
            messages.success(
                request,
                f"Patient {patient.username} has been enabled."
            )
        else:
            messages.success(
                request,
                f"Patient {patient.username} has been disabled."
            )

    return redirect("manage_patients")