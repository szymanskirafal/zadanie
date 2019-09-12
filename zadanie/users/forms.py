from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django_registration.forms import RegistrationForm

from .models import CustomUser


class CustomUserForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ('email', 'username',)


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = get_user_model()
        fields = ('email', 'username',)
