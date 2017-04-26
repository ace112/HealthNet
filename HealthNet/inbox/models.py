from django.db import models
from django.conf import settings
from datetime import datetime
from core.models import Log
from django.conf import settings

# Create your models here.


class Inbox(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='receiver')
    message = models.TextField(max_length=50)
    todel = models.BooleanField(default=False)
    fromdel = models.BooleanField(default=False)

    def delcheck(self):
        if self.todel == True and self.fromdel == True:
            self.delete()

