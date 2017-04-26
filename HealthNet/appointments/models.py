from django.db import models
from django.conf import settings
from core.models import Log


class Appointment(models.Model):
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='doctor')
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='patient')
    time = models.DateTimeField()
    message = models.TextField()

    def __str__(self):
        return self.time.strftime("%m/%d/%Y %H:%M")

    def delete(self, using=None, keep_parents=False):
        Log.objects.create(log_type='delete appointment', description="Appointment was deleted")
        super(Appointment, self).delete()