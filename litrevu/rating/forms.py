from django import forms

from . import models


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ("title", "description", "image")


class ReviewForm(forms.ModelForm):
    # user chose a rating using a radio button
    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(6)], widget=forms.RadioSelect, label="Note"
    )

    class Meta:
        model = models.Review
        fields = ("headline", "rating", "body")
