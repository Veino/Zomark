from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import ZomarkUser


class ZomarkUserCreationForm(UserCreationForm):

    class Meta:
        model = ZomarkUser
        fields = ("email",)


class ZomarkUserChangeForm(UserChangeForm):

    class Meta:
        model = ZomarkUser
        fields = ("email",)