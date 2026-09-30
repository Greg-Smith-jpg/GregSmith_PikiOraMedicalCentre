from django import forms
from .models import Doctor


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            "name",
            "speciality",
            "email",
            "phone",
            "description"
        ]


class AppointmentBookingForm(forms.Form):
    reason = forms.CharField(
        required=True,
        max_length=500,
        widget=forms.Textarea(attrs={
            "rows": 4,
            "placeholder": "Please enter the reason for your appointment."
        })
    )


class AppointmentReasonForm(forms.Form):
    reason = forms.CharField(
        required=True,
        max_length=500,
        widget=forms.Textarea(attrs={
            "rows": 4
        })
    )