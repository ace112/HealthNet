from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse_lazy
from .models import Prescription
from core.models import User, Hospital



class BaseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.hospital = Hospital.objects.create(name='Test')

        self.user = User.objects.create_user('test@test.com', 'test@test.com', '123pass321pass')

    def log_in(self):
        return self.client.login(username=self.user.username, password='123pass321pass')


class PrescriptionCreation(TestCase):

    def test_valid(self):
        from .forms import PrescriptionCreateForm

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
            'medication': 'Motrin'
        }
        form = PrescriptionCreateForm(data=data, user=doctor, pat=patient)
        self.assertTrue(form.is_valid())
        instance = form.save()
        self.assertEqual(Prescription.objects.get(id=instance.id), instance)

    def test_invalid(self):
        from .forms import PrescriptionCreateForm

        patient = User.objects.create_user('test@test.com', 'test@test.com', '123pass321pass')
        doctor = User.objects.create_user('doc@test.com', 'doc@test.com', '123pass321pass')
        patient.user_type = 'PA'
        doctor.user_type = 'DO'
        doctor.save()
        patient.save()

        data = {
            'doctor': doctor.id,
            'patient': patient.id,
            'time': "",
            'medication': 'Motrin'
        }
        form = PrescriptionCreateForm(data=data, user=doctor, pat=patient)
        self.assertFalse(form.is_valid())
        self.assertIn('time', form.errors)


class PrescriptionDeletion(TestCase):

    def test_valid(self):
        from .forms import PrescriptionCreateForm

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
            'medication': 'Motrin'
        }
        form = PrescriptionCreateForm(data=data, user=doctor, pat=patient)
        form.save()
        Prescription.objects.get(id=1).delete()
        self.assertFalse(Prescription.objects.filter(id=1).exists())

# class StatisticsTests(BaseTestCase):
#
#     def test_must_be_logged_in(self):
#         response = self.client.get(reverse_lazy('stats'))
#         self.assertEqual(response.status_code, 302)
#
#     def test_admin(self):
#         self.user.user_type = 'AD'
#         self.user.save()
#         self.log_in()
#         response = self.client.get(reverse_lazy('stats'))
#         self.assertEqual(response.status_code, 200)
#
#     def test_not_admin(self):
#         self.user.user_type = 'PA'
#         self.user.save()
#         self.log_in()
#         response = self.client.get(reverse_lazy('stats'))
#         self.assertEqual(response.status_code, 302)
