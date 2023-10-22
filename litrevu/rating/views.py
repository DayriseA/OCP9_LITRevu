from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from . import forms, models


@login_required
def feed(request):
    tickets = models.Ticket.objects.all()
    return render(request, "rating/feed.html", {"tickets": tickets})


def ticket_create(request):
    form = forms.TicketForm()
    if request.method == "POST":
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.author = request.user
            ticket.save()
            return redirect("feed")
    return render(request, "rating/ticket_create.html", {"form": form})
