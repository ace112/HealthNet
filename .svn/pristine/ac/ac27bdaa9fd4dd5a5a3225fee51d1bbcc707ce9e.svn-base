from django import forms
from .models import Appointment
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
User = get_user_model()


class AppointmentCreateForm(forms.ModelForm):
    patient = forms.ModelChoiceField(queryset=User.objects.filter(user_type='PA'))
    doctor = forms.ModelChoiceField(queryset=User.objects.filter(user_type='DO'))

    class Meta:
        model = Appointment
        fields = (
            'doctor',
            'patient',
            'time',
            'message'
        )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AppointmentCreateForm, self).__init__(*args, **kwargs)
        if user.user_type == 'PA':
            self.fields['patient'].initial = user.id
            self.fields['patient'].disabled = True
        if user.user_type == 'DO':
            self.fields['doctor'].initial = user.id
            self.fields['doctor'].disabled = True
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'

    def clean(self):
        clean_data = super(AppointmentCreateForm, self).clean()
        if Appointment.objects.filter((Q(doctor=clean_data.get('doctor')) | Q(patient=clean_data.get('patient'))) &
                Q(time=clean_data.get('time'))).exists():
            msg = "Already an appointment at this time"
            self.add_error('time', msg)


