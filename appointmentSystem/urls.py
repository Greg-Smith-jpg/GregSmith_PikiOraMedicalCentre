from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("register/", views.register, name="register"),
    path('doctors/', views.doctors, name='doctors'),
    path('doctors/<int:doctor_id>/', views.doctor_slots, name='doctor_slots'),
    path("appointments/book/<int:slot_id>", views.book_appointment, name="book_appointment"),
    path("appointments/", views.my_appointments, name="my_appointments"),
    path("appointments/cancel/<int:appointment_id>", views.cancel_appointment, name="cancel_appointment"),
    path("appointments/edit-reason/<int:appointment_id>/", views.edit_reason, name="edit_reason"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-dashboard/doctors/add", views.add_doctor, name="add_doctor"),
    path("admin-dashboard/doctors/edit/<int:doctor_id>/", views.edit_doctor, name="edit_doctor"),

    path(
        "admin-dashboard/doctors/delete/<int:doctor_id>/", views.delete_doctor, name="delete_doctor"),
    path(
        "admin-dashboard/doctors/<int:doctor_id>/slots/",
        views.manage_slots,
        name="manage_slots"
    ),

    path(
        "admin-dashboard/doctors/<int:doctor_id>/slots/add/",
        views.add_slot,
        name="add_slot"
    ),

    path(
        "admin-dashboard/slots/edit/<int:slot_id>/",
        views.edit_slot,
        name="edit_slot"
    ),

    path(
        "admin-dashboard/slots/delete/<int:slot_id>/",
        views.delete_slot,
        name="delete_slot"
    ),
    path(
        "admin-dashboard/appointments/",
        views.admin_appointments,
        name="admin_appointments"
    ),
    path(
        "admin-dashboard/appointments/edit/<int:appointment_id>/",
        views.admin_edit_appointment,
        name="admin_edit_appointment"
    ),
    path(
        "admin-dashboard/appointments/cancel/<int:appointment_id>/",
        views.admin_cancel_appointment,
        name="admin_cancel_appointment"
    ),

    path(
        "admin-dashboard/patients/",
        views.manage_patients,
        name="manage_patients"
    ),
    path(
        "admin-dashboard/patients/toggle/<int:patient_id>/",
        views.toggle_patient_status,
        name="toggle_patient_status"
    ),
]
