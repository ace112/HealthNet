from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse_lazy
from .models import Appointment
from core.models import User


class AppointmentCreation(TestCase):

    def test_valid(self):
        from .forms import AppointmentCreateForm

        patient = User.objects.create_user('test@test.com', 'test@test.com', '123pass321pass')
        doctor = User.objects.create_user('doc@test.com', 'doc@test.com', '123pass321pass')
        patient.user_type = 'PA'
        doctor.user_type = 'DO'
        doctor.save()
        patient.save()

        data = {
            'doctor': doctor.id,
            'patient': patient.id,
            'time': "2017-12-12 16:11:31.963644",
            'message': 'Hello',
        }
        form = AppointmentCreateForm(data=data, user=doctor)
        self.assertTrue(form.is_valid())
        instance = form.save()
        self.assertEqual(Appointment.objects.get(id=instance.id), instance)


class AppointmentUpdate(TestCase):

    def test_valid(self):
        from .forms import AppointmentCreateForm

        patient = User.objects.create_user('test@test.com', 'test@test.com', '123pass321pass')
        doctor = User.objects.create_user('doc@test.com', 'doc@test.com', '123pass321pass')
        patient.user_type = 'PA'
        doctor.user_type = 'DO'
        doctor.save()
        patient.save()

        data = {
            'doctor': doctor.id,
            'patient': patient.id,
            'time': "2017-12-12 16:11:31.963644",
            'message': 'Hello',
        }
        form = AppointmentCreateForm(data=data, user=doctor)
        form.data['message'] = "Hi"
        form.data['time'] = "2017-11-11 16:11:31.963644"
        self.assertTrue(form.is_valid())
        instance = form.save()
        self.assertEqual(Appointment.objects.get(id=instance.id), instance)

    def test_invalid(self):
        from .forms import AppointmentCreateForm

        patient = User.objects.create_user('test@test.com', 'test@test.com', '123pass321pass')
        doctor = User.objects.create_user('doc@test.com', 'doc@test.com', '123pass321pass')
        patient.user_type = 'PA'
        doctor.user_type = 'DO'
        doctor.save()
        patient.save()

        data = {
            'doctor': doctor.id,
            'patient': patient.id,
            'time': "2017-12-12 16:11:31.963644",
            'message': 'Hello',
        }
        form = AppointmentCreateForm(data=data, user=doctor)
        form.data['message'] = "Hi"
        form.data['time'] = ""
        self.assertFalse(form.is_valid())
        self.assertIn('time', form.errors)

