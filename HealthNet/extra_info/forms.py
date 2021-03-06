from django import forms
from .models import Prescription, Test
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import datetime
User = get_user_model()


class PrescriptionCreateForm(forms.ModelForm):
    patient = forms.ModelChoiceField(queryset=User.objects.filter(user_type='PA'))
    doctor = forms.ModelChoiceField(queryset=User.objects.filter(user_type='DO'))

    class Meta:
        model = Prescription
        fields = (
            'doctor',
            'patient',
            'time',
            'medication'
        )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        pat = kwargs.pop('pat', None)
        super(PrescriptionCreateForm, self).__init__(*args, **kwargs)
        if user.user_type == 'DO':
            self.fields['doctor'].initial = user.id
            self.fields['doctor'].disabled = True
            self.fields['patient'].initial = pat.id
            self.fields['patient'].disabled = True
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'


class TestCreateForm(forms.ModelForm):
    subject = forms.ModelChoiceField(queryset=User.objects.filter(user_type='PA'))

    class Meta:
        model = Test
        fields = (
            'subject',
            'time',
            'description',
            'released',
            'comments',
            'image'
        )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        patient_id = int(kwargs.pop('patient_id'))
        super(TestCreateForm, self).__init__(*args, **kwargs)
        self.fields['subject'].initial = patient_id
        self.fields['subject'].disabled = True
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

