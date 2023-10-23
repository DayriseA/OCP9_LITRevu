from django import forms

from . import models


class TicketForm(forms.ModelForm):
    title = forms.CharField()
    title.widget.attrs["class"] = "size-auto"

    class Meta:
        model = models.Ticket
        fields = ("title", "description", "image")


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ("headline", "rating", "body")
