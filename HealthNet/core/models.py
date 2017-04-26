from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)

USER_TYPES = (
    ('DO', 'Doctor'),
    ('NU', 'Nurse'),
    ('PA', 'Patient'),
    ('AD', 'Administrator'),
)


class Hospital(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name

    def average_patient_per_day(self):
        # return all extended stay within hospital
        stays = ExtendedStay.objects.filter(user__hospital=self)
        count = dict()
        for i in stays:
            if i.start.date().__str__() in count:
                count[i.start.date().__str__()] += 1
            else:
                count[i.start.date().__str__()] = 0

        if len(count.values()) == 0:
            return 0

        return sum(count.values())/len(count.values())

    def average_visits(self):
        # return all extended stay within hospital
        vists = ExtendedStay.objects.filter(user__hospital=self).count()
        users = User.objects.filter(
            hospital=self,
            user_type='PA'
        ).count()

        if users == 0:
            return 0

        return vists/users

    def average_duration(self):
        from django.db.models import Avg
        import datetime
        # return all extended stay within hospital

        times = ExtendedStay.objects.filter(user__hospital=self).values_list('duration', flat=True)
        if len(times) == 0:
            return 0
        td = sum(times, datetime.timedelta(0))/len(times)
        days, hours, minutes = td.days, td.seconds // 3600, td.seconds // 60 % 60
        return "{} D, {} H, {} M".format(days, hours, minutes)

    def average_prescriptions(self):
        # return all extended stay within hospital
        from extra_info.models import Prescription
        prescriptions = Prescription.objects.filter(
            patient__hospital=self
        ).count()

        users = User.objects.filter(
            hospital=self,
            user_type='PA'
        ).count()

        if users == 0:
            return 0

        return prescriptions/users

    def most_common_reason(self):
        stays = ExtendedStay.objects.filter(user__hospital=self)
        if stays.count() == 0:
            return "N/A"
        items = dict()
        for i in stays:
            reason = i.reason.lower()
            if reason in items:
                items[reason] += 1
            else:
                items[reason] = 0
        return max(items, key=items.get).title()


class User(AbstractUser):
    user_type = models.CharField(
        max_length=2,
        choices=USER_TYPES,
        default='PA',
    )
    hospital = models.ForeignKey(Hospital, null=True, blank=True)
    unread = models.IntegerField(default=0, null=True, blank=True)

    # Medical info
    insurance = models.CharField(max_length=80, null=True, blank=True )
    address = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    emergency_contact_email = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(11),
                                       MaxValueValidator(11)], help_text='Format: 99999999999')
    weight = models.IntegerField(validators=[MinValueValidator(0),
                                       MaxValueValidator(999)], blank=True, null=True)
    height = models.IntegerField(null=True, blank=True, help_text="Height in Inches", validators=[MinValueValidator(0),
                                       MaxValueValidator(99)])
    birthday = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return self.email

    @property
    def get_user_type(self):
        return dict(USER_TYPES)[self.user_type]

    @property
    def is_admitted(self):
        return ExtendedStay.objects.filter(user=self, end=None).exists()

    def save(self, *args, **kwargs):
        if self.pk is None:
            Log.objects.create(log_type='create user',
                               description="User was created with email " + self.email)

        self.username = self.email
        self.is_staff = (self.user_type == 'AD' or self.is_superuser)
        if self.is_staff:
            self.user_type = 'AD'
        super(User, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        Log.objects.create(user=self, log_type='delete user', description="User was deleted with email " + self.email)
        super(User, self).delete()

    @property
    def get_emergency_contact(self):
        # check if user is in system

        user = User.objects.filter(email=self.emergency_contact_email)
        if user.exists():
            user = user[0]
            string = user.email
            for att in ['first_name', 'last_name', 'phone']:
                a = getattr(user, att)
                if a != '' and a != None:
                    string += ', {}'.format(a)

            return string

        return self.emergency_contact_email


User._meta.get_field('email')._unique = True
User._meta.get_field('username')._unique = True


class ExtendedStay(models.Model):
    user = models.ForeignKey(User)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(blank = True, null = True)
    duration = models.DurationField(blank = True, null = True)
    reason = models.CharField(max_length=15)

    # Actual magic has occurred here
    def save(self, *args, **kwargs):
        if self.end:
            self.duration = self.end - self.start
        super(ExtendedStay, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.email


class Log(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    log_type = models.CharField(max_length=10)
    description = models.CharField(max_length=140)
