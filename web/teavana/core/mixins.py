from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied


class UserRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account_login')
        else:
            return super().dispatch(request, *args, **kwargs)


class StaffRequiredMixin:
    """Mixin that requires the user to be staff to access."""
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class AdminRequiredMixin:
    """Mixin that requires the user to be admin to access."""
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
