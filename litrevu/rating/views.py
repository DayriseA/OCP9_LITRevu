from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from . import forms, models


@login_required
def feed(request):
    tickets = models.Ticket.objects.all()
    reviews = models.Review.objects.all()
    context = {"tickets": tickets, "reviews": reviews}
    return render(request, "rating/feed.html", context=context)


@login_required
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


@login_required
def review_create(request):
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()
    if request.method == "POST":
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        # use all() to assure errors are displayed for both forms
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.author = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.author = request.user
            review.save()
            return redirect("feed")
    context = {"ticket_form": ticket_form, "review_form": review_form}
    return render(request, "rating/review_create.html", context=context)
