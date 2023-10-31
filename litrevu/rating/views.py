from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from itertools import chain
from django.core.paginator import Paginator

from . import forms, models


@login_required
def feed(request):
    """Display the feed of tickets and reviews."""
    tickets = models.Ticket.objects.all()
    reviews = models.Review.objects.all()
    # chain tickets and reviews together and sort them by time_created, newest first
    feed = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True,
    )
    # paginate the feed
    paginator = Paginator(feed, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "rating/feed.html", {"page_obj": page_obj})


@login_required
def my_posts(request):
    """Display the tickets and reviews posted by the user."""
    tickets = models.Ticket.objects.filter(author=request.user)
    reviews = models.Review.objects.filter(author=request.user)
    feed = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True,
    )
    paginator = Paginator(feed, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "rating/my_posts.html", {"page_obj": page_obj})


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
def review_create(request, ticket_id=None):
    """
    Create a review for a ticket. If no ticket_id is provided, a ticket must be
    created in the process.
    """
    # ticket as None for context when no ticket_id is provided
    ticket = None
    # ticket_form as None for context when ticket_id is provided
    ticket_form = None
    review_form = forms.ReviewForm()

    if ticket_id:
        ticket = get_object_or_404(models.Ticket, id=ticket_id)

    if not ticket_id:
        ticket_form = forms.TicketForm()

    if request.method == "POST":
        review_form = forms.ReviewForm(request.POST)
        # if no ticket_id then we have a ticket_form to process
        if not ticket_id:
            ticket_form = forms.TicketForm(request.POST, request.FILES)
            # we don't want to save ticket_form if review_form is invalid
            if all([ticket_form.is_valid(), review_form.is_valid()]):
                ticket = ticket_form.save(commit=False)
                ticket.author = request.user
                ticket.save()

        if all([review_form.is_valid(), ticket]):
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.author = request.user
            review.save()
            return redirect("feed")
    context = {"ticket_form": ticket_form, "review_form": review_form, "ticket": ticket}
    return render(request, "rating/review_create.html", context=context)


@login_required
def ticket_edit(request, ticket_id):
    """Edit a ticket. Only the author of the ticket can edit it."""
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    # check if the user is the author of the ticket
    if request.user == ticket.author:
        form = forms.TicketForm(instance=ticket)
        if request.method == "POST":
            form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
            if form.is_valid():
                form.save()
                return redirect("my_posts")
        context = {"form": form, "ticket": ticket}
        return render(request, "rating/ticket_edit.html", context=context)
    elif request.user != ticket.author:
        messages.error(request, "Vous n'avez pas le droit de modifier ce ticket.")
        return redirect("feed")


@login_required
def review_edit(request, review_id):
    """Edit a review. Only the author of the review can edit it."""
    review = get_object_or_404(models.Review, id=review_id)
    # check if the user is the author of the review
    if request.user == review.author:
        form = forms.ReviewForm(instance=review)
        ticket = review.ticket
        if request.method == "POST":
            form = forms.ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                return redirect("my_posts")
        context = {"form": form, "ticket": ticket}
        return render(request, "rating/review_edit.html", context=context)
    elif request.user != review.author:
        messages.error(request, "Vous n'avez pas le droit de modifier cette critique.")
        return redirect("feed")


@login_required
def ticket_delete(request, ticket_id):
    """Delete a ticket. Only the author of the ticket can delete it."""
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if request.user == ticket.author:
        ticket.delete()
        messages.success(request, "Ticket supprimé avec succès.")
    # if the user is not the author of the ticket, send an error message
    elif request.user != ticket.author:
        messages.error(request, "Vous n'avez pas la permission de supprimer ce ticket.")
    return redirect("my_posts")


@login_required
def review_delete(request, review_id):
    """Delete a review. Only the author of the review can delete it."""
    review = get_object_or_404(models.Review, id=review_id)
    if request.user == review.author:
        review.delete()
        messages.success(request, "Critique supprimée avec succès.")
    # if the user is not the author of the review, send an error message
    elif request.user != review.author:
        messages.error(
            request, "Vous n'avez pas la permission de supprimer cette critique."
        )
    return redirect("my_posts")
