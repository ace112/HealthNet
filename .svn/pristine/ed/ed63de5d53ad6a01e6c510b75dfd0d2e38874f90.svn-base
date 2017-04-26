from django.core.exceptions import PermissionDenied

class AdministratorMixin(object):
    

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated() or request.user.user_type != 'AD':
            raise PermissionDenied

        return super(AdministratorMixin, self).dispatch(request, *args, **kwargs)
