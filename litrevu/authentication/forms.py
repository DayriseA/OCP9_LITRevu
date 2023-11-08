from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "password1", "password2")


class MyAuthForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "password"]

    def __init__(self, *args, **kwargs):
        super(MyAuthForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = False
        self.fields["username"].widget = forms.TextInput(
            attrs={
                "class": "form-control text-center",
                "placeholder": "Nom d'utilisateur",
            }
        )
        self.fields["password"].label = False
        self.fields["password"].widget = forms.PasswordInput(
            attrs={"class": "form-control text-center", "placeholder": "Mot de passe"}
        )
