from django.shortcuts import redirect

class UserRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return reverse('account_login')
        else:
            return super().dispatch(request, *args, **kwargs)
