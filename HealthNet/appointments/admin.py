from django.contrib import admin
from .models import Appointment
from django.contrib.auth import get_user_model

User = get_user_model()

# Register your models here.
class AppointmentAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(AppointmentAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['doctor'].queryset = User.objects.filter(user_type='DO')
        form.base_fields['patient'].queryset = User.objects.filter(user_type='PA')
        return form


admin.site.register(Appointment, AppointmentAdmin)
