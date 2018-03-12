from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from gears.models import Farm


class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form):
        user = super().save_user(request, user, form)
        Farm.objects.create_default(user)
        return user


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form=form)
        Farm.objects.create_default(user)
        return user
