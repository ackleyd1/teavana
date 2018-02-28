from carts.models import Cart

from allauth.account.adapter import DefaultAccountAdapter

class AccountAdapter(DefaultAccountAdapter):
    def new_user(self, request):
        user = super().new_user(request)
        Cart.objects.get_or_create(user=user)
        return user
