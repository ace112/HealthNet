from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from .forms import UserCreateForm, TransferForm, AdmissionForm, DismissalForm
from django.forms import ModelForm
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.response import TemplateResponse
from .mixins import PatientMixin, LoginRedirectMixin, DoctorMixin, DoctorNurseMixin
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.exceptions import ValidationError
from extra_info.models import Prescription, Test
from appointments.models import Appointment
from .models import Log, ExtendedStay
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.utils import timezone
from django.template.response import TemplateResponse
User = get_user_model()


TEMPLATE = 'errors/error.html'
# Create your views here.


class SignUpView(LoginRedirectMixin, CreateView):
    model = User
    template_name = 'registration/register.html'
    success_url = reverse_lazy('dashboard')
    form_class = UserCreateForm

    def form_valid(self, form):
        # save the new user first
        form.save()
        # get the username and password
        username = self.request.POST['email']
        password = self.request.POST['password1']
        # authenticate user then login
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(SignUpView, self).form_valid(form)


# @method_decorator(csrf_exempt, name='dispatch')
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        if self.request.user.user_type == 'DO' or self.request.user.user_type == 'NU':
            context['accessible_users'] = User.objects.filter(user_type='PA')
        elif self.request.user.user_type != 'AD':
            context['available_actions'] = [
                ('View Calendar', reverse('calendar')),
                ('Update Profile', reverse('profile', args=[self.request.user.id])),
            ]
            context['available_actions'].append((
                    'View Medical Information', reverse('medical')
                ))
        return context


class MedicalInfoView(LoginRequiredMixin, PatientMixin, TemplateView):
    template_name = 'medical_info.html'

    def get(self, request, *args, **kwargs):
        Log.objects.create(log_type='view medical info', description="Medical info was viewed")
        return super(MedicalInfoView, self).get(request, *args, **kwargs)


def download(request):
    user = request.user
    response = HttpResponse("", content_type='text/plain');
    response['Content-Disposition'] = 'attachment; filename="medical_info.txt"'
    response.flush()
    prescriptions = Prescription.objects.filter(patient=user).order_by('time')
    appointments = Appointment.objects.filter(patient=user).order_by('time')
    stays = ExtendedStay.objects.filter(user=user).order_by('start')
    tests = Test.objects.filter(subject=user, released=True).order_by('time')
    lines = []
    lines.append("Medical profile for " + user.first_name + " " + user.last_name + "\r\n")
    lines.append("\r\n==Basic Info==\r\n")
    lines.append("Insurance: " + user.insurance + "\r\n")
    lines.append("Address: " + user.address + "\r\n")
    lines.append("Phone number: " + user.phone + "\r\n")
    lines.append("Emergency contact: " + user.get_emergency_contact + "\r\n")
    lines.append("Weight: " + user.weight + "\r\n")
    lines.append("Height: " + user.height + "\r\n")
    lines.append("Date of birth: " + str(user.birthday) + "\r\n")
    lines.append("\r\n==Current Prescriptions==\r\n")
    for prescription in prescriptions:
        lines.append("" + prescription.medication + " prescribed by " + prescription.doctor.first_name +
                     " " + prescription.doctor.last_name + " on " + str(prescription.time) + "\r\n")
    lines.append("\r\n==Appointment Record==\r\n")
    for appointment in appointments:
        lines.append("Appointment with " + appointment.doctor.first_name +
                     " " + appointment.doctor.last_name + " at " + str(appointment.time) + "\r\n")
    lines.append("\r\n==Hospital Stays==\r\n")
    for stay in stays:
        lines.append("Admitted: " + str(stay.start) + " Discharged: " + str(stay.end) +
                     ", Reason: " + stay.reason + "\r\n")
    lines.append("\r\n==Test Results==\r\n")
    for test in tests:
        lines.append("" + str(test.time) + ": " + test.description + "\r\n")
    response.writelines(lines)
    return response


class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email', 'gender', 'phone', 'address', 'birthday']
    template_name = 'update_profile_info.html'
    success_url = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):

        Log.objects.create(log_type='view profile', description="User's profile was viewed: " + User.objects.get(
            pk=kwargs.get('pk')).email)

        if int(kwargs['pk']) != self.request.user.pk:
            return TemplateResponse(request, 'errors/error.html')

        if self.request.user.user_type == 'PA':
            self.fields.append('emergency_contact_email')

        if self.request.user.user_type == 'AD' and not self.request.user.hospital:
            self.fields.append('hospital')

        return super(UpdateProfile, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        Log.objects.create(log_type='update user profile', description="User was updated with email: " +
                                                                       self.request.user.email)
        return super(UpdateProfile, self).form_valid(form)


class UpdateMedicalInfo(LoginRequiredMixin, DoctorMixin, UpdateView):
    model = User
    fields = ['insurance', 'address', 'phone', 'weight', 'height', 'birthday']
    template_name = 'update_medical.html'
    success_url = reverse_lazy('dashboard')
    context_object_name = 'user2'

    def form_valid(self, form):
        Log.objects.create(
            log_type='update medical info',
            description="Medical info was updated: " + self.request.user.email
        )
        return super(UpdateMedicalInfo, self).form_valid(form)


class TransferView(LoginRequiredMixin, DoctorMixin, UpdateView):
    model = User
    template_name = 'transfer.html'
    success_url = reverse_lazy('dashboard')
    form_class = TransferForm
    context_object_name = 'user2'

    def form_valid(self, form):
        Log.objects.create(log_type='transfer', description="Patient was transferred: " + self.request.user.email)
        return super(TransferView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(user=self.request.user)

        return kwargs


class AdmitView(LoginRequiredMixin,DoctorNurseMixin,UpdateView):
    model = User
    template_name = 'admit.html'
    success_url = reverse_lazy('dashboard')
    form_class = AdmissionForm
    context_object_name = 'user2'

    # Verifies action
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().is_admitted:
            return TemplateResponse(request, TEMPLATE)

        return super(AdmitView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
            Log.objects.create(log_type='admit', description="Patient was admitted: " + self.request.user.email)
            ExtendedStay.objects.create(user=self.get_object(), start = datetime.now(), reason=form.cleaned_data.get('reason'))
            return super(AdmitView, self).form_valid(form)


class DischargeView(LoginRequiredMixin, DoctorMixin, UpdateView):
    model = User
    template_name= 'discharge.html'
    success_url = reverse_lazy('dashboard')
    form_class = DismissalForm
    context_object_name = 'user2'

    # Verifies action
    def dispatch(self, request, *args, **kwargs):
        if not self.get_object().is_admitted:
            return TemplateResponse(request, TEMPLATE)

        return super(DischargeView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        Log.objects.create(log_type='discharge', description="Patient was discharged: " + self.request.user.email)
        stay = ExtendedStay.objects.filter(user=self.object, end=None).first()
        stay.end = timezone.now()
        stay.save()
        return super(DischargeView, self).form_valid(form)