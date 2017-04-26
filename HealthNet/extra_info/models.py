from django.db import models
from django.conf import settings
from datetime import datetime
from core.models import Log
from HealthNet.settings import MEDIA_ROOT
from django.conf import settings

# Create your models here.


class Prescription(models.Model):
    medication = models.TextField()
    time = models.DateTimeField(default=datetime.now)
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='patient_prescription')
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='doctor_prescription')

    def __str__(self):
        return self.patient.first_name + " " + self.patient.last_name

    def delete(self, using=None, keep_parents=False):
        Log.objects.create(log_type='delete prescription', description="Prescription was deleted")
        super(Prescription, self).delete()


class Test(models.Model):
    subject = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='subject')
    time = models.DateTimeField(default=datetime.now)
    description = models.CharField(max_length=200)
    comments = models.TextField(blank=True)
    released = models.BooleanField(default=False, help_text="(Allow patient to view these test results)")
    image = models.FileField(upload_to='', null=True, blank=True)
