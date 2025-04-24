from django.forms import ModelForm
from .models import Vet

class AppointmentForm(ModelForm):
    class Meta:
        model = Vet
        fields = ['clinic', 'appointment', 'nurse_name']