from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    # customize by overriding the fields directly (code cleaner and easier to read
    # compared to overriding __init__ method)
    username = forms.CharField(
        label=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nom d'utilisateur",
                "class": "form-control text-center",
            }
        ),
        help_text=None,
    )
    password1 = forms.CharField(
        label=False,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Mot de passe", "class": "form-control text-center"}
        ),
        help_text=None,
    )
    password2 = forms.CharField(
        label=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirmer mot de passe",
                "class": "form-control text-center",
            }
        ),
        help_text=None,
    )

    class Meta:
        model = get_user_model()
        fields = ("username", "password1", "password2")


class MyAuthForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "password"]

    # customize the form by overriding __init__ method (recommended when you want to
    # reuse the code by creating a base form class and inheriting from it.)
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
