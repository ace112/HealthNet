from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Appointment
from .forms import AppointmentCreateForm
from core.mixins import DoctorPatientMixin, NurseMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.template.response import TemplateResponse
from core.models import Log
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django import forms
# Create your views here.


class CreateAppointment(LoginRequiredMixin, CreateView):
    model = Appointment
    template_name = 'create_appointment.html'
    success_url = reverse_lazy('calendar')
    form_class = AppointmentCreateForm

    def form_valid(self, form):
        Log.objects.create(log_type='create appointment', description="Appointment was created: " +
                                                                      self.request.user.email)
        return super(CreateAppointment, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(user=self.request.user)

        return kwargs


class Calendar(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super(Calendar, self).get_context_data(**kwargs)
        if self.request.user.user_type == 'NU':
            context['appointments'] = Appointment.objects.filter(
                Q(patient__hospital=self.request.user.hospital) or
                Q(doctor__hospital=self.request.user.hospital)
            ).order_by('time')
        else:
            context['appointments'] = Appointment.objects.filter(Q(patient=self.request.user.id) |
                                                                 Q(doctor=self.request.user.id)).order_by('time')
        return context


class DeleteAppointment(LoginRequiredMixin, DeleteView):
    model = Appointment
    success_url = reverse_lazy('calendar')
    template_name = 'appointment_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if self.request.user.id not in ([obj.doctor.id] + [obj.patient.id]):
            return TemplateResponse(request, 'errors/error.html')

        return super(DeleteAppointment, self).dispatch(request, *args, **kwargs)


class UpdateAppointment(LoginRequiredMixin, UpdateView):
    model = Appointment
    fields = ['time', 'message']
    success_url = reverse_lazy('calendar')
    template_name = "update_appointment.html"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if self.request.user.id not in ([obj.doctor.id] + [obj.patient.id]) and self.request.user.user_type != 'NU':
            return TemplateResponse(request, 'errors/error.html')

        return super(UpdateAppointment, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        Log.objects.create(log_type='update appointment', description="Appointment was updated: " +
                                                                      self.request.user.email)
        return super(UpdateAppointment, self).form_valid(form)
