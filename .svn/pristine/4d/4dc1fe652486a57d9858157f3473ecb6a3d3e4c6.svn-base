from django.contrib import admin
from .models import Test, Prescription

# Register your models here.


class PrescriptionAdmin(admin.ModelAdmin):
    #readonly_fields = ('patient', 'doctor',)
    list_display = ('time', 'patient', 'doctor',)
    ordering = ('time',)


class TestAdmin(admin.ModelAdmin):
    #readonly_fields = ('subject',) TODO Either restrict choices to patients when editing Tests or prevent admin from creating Tests
    list_display = ('time', 'subject',)
    ordering = ('time',)

admin.site.register(Prescription, PrescriptionAdmin)
admin.site.register(Test, TestAdmin)