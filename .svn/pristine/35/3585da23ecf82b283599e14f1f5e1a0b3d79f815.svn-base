from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView
from django.template.response import TemplateResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


TEMPLATE = 'errors/error.html'

class DoctorMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated() or request.user.user_type != 'DO':
            return TemplateResponse(request, TEMPLATE)

        return super(DoctorMixin, self).dispatch(request, *args, **kwargs)

class PatientMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated() or request.user.user_type != 'PA':
            return TemplateResponse(request, TEMPLATE)

        return super(PatientMixin, self).dispatch(request, *args, **kwargs)

class DoctorNurseMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated() or (request.user.user_type != 'DO' and request.user.user_type != 'NU'):
            return TemplateResponse(request, TEMPLATE)

        return super(DoctorNurseMixin, self).dispatch(request, *args, **kwargs)

class NurseMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated() or request.user.user_type != 'NU':
            return TemplateResponse(request, TEMPLATE)

        return super(NurseMixin, self).dispatch(request, *args, **kwargs)

class AdminMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated() or request.user.user_type != 'AD':
            return TemplateResponse(request, TEMPLATE)

        return super(AdminMixin, self).dispatch(request, *args, **kwargs)

class DoctorPatientMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated() or (request.user.user_type != 'DO' and request.user.user_type != 'PA'):
            return TemplateResponse(request, TEMPLATE)

        return super(DoctorPatientMixin, self).dispatch(request, *args, **kwargs)

class LoginRedirectMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('dashboard')

        return super(LoginRedirectMixin, self).dispatch(request, *args, **kwargs)
