from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.shortcuts import render, redirect, get_object_or_404
from itertools import chain

from . import forms, models

User = get_user_model()


@login_required
def feed(request):
    """
    Display a feed of tickets and reviews. Composed of posts from followed users,
    from the user, and reviews responding to the user's tickets.
    (Be warned that a new user will start with an empty feed)
    """
    user = request.user
    users_followed = user.follows.all()
    # tickets (not reviewed by same author) and reviews from followed users
    tickets_followed = models.Ticket.objects.filter(author__in=users_followed).exclude(
        Q(review__author=F("author"))
    )
    reviews_followed = models.Review.objects.filter(author__in=users_followed)

    # tickets (not already reviewed by the user) and reviews from the user
    user_tickets = models.Ticket.objects.filter(author=user).exclude(
        Q(review__author=user)
    )
    user_reviews = models.Review.objects.filter(author=user)

    # reviews responding to the user's tickets but not written by the user
    responding_reviews = models.Review.objects.filter(ticket__author=user).exclude(
        author=user
    )

    # combine all into a single feed
    feed = sorted(
        chain(
            tickets_followed,
            reviews_followed,
            user_tickets,
            user_reviews,
            responding_reviews,
        ),
        key=lambda instance: instance.time_created,
        reverse=True,
    )
    # paginate the feed
    paginator = Paginator(feed, 4)
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
    paginator = Paginator(feed, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "rating/my_posts.html", {"page_obj": page_obj})


@login_required
def ticket_create(request):
    """Create a ticket."""
    form = forms.TicketForm()
    if request.method == "POST":
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            # commit=False to prevent saving the form before adding the author
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


@login_required
def follows(request):
    """
    Allow the user to follow an other using an input with its username.
    Displays a list of followed users, followers and blocked users.
    """
    user = request.user
    following = user.follows.all()  # users followed by the user
    followers = user.followers.all()  # users following the user
    blocked_users = user.blocks.all()  # users blocked by the user

    if request.method == "POST":
        username = request.POST.get("username")
        try:
            user_to_follow = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Cet utilisateur n'existe pas.")
            return redirect("follows")
        # check if the user is not trying to follow himself
        if user_to_follow == user:
            messages.error(request, "Vous ne pouvez pas vous suivre vous-même.")
            return redirect("follows")
        # check if the user is not already following the user_to_follow
        if user_to_follow in user.follows.all():
            messages.error(request, "Vous suivez déjà cet utilisateur.")
            return redirect("follows")
        # check if the user_to_follow has not blocked the user
        if user in user_to_follow.blocks.all():
            messages.error(request, "Vous avez été bloqué par cet utilisateur.")
            return redirect("follows")
        # add the user_to_follow to the user's following
        user.follows.add(user_to_follow)
        messages.success(request, f"Vous suivez maintenant {user_to_follow.username}.")
        return redirect("follows")

    context = {"following": following, "followers": followers, "blocked": blocked_users}
    return render(request, "rating/follows.html", context=context)


@login_required
def unfollow(request, user_id):
    """Unfollow a user from the follows page."""
    user_to_unfollow = get_object_or_404(User, id=user_id)
    user = request.user
    if user_to_unfollow in user.follows.all():
        user.follows.remove(user_to_unfollow)
        messages.success(request, f"Vous ne suivez plus {user_to_unfollow.username}.")
    return redirect("follows")


@login_required
def block_user(request, user_id):
    """Block a follower. Use to prevent a user from seeing your posts."""
    user_to_block = get_object_or_404(User, id=user_id)
    user = request.user
    # prevent blocking yourself
    if user_to_block == request.user:
        messages.error(request, "Vous ne pouvez pas vous bloquer vous-même.")
        return redirect("follows")
    # check if the user is already blocked
    if user_to_block in request.user.blocks.all():
        messages.error(request, "Vous avez déjà bloqué cet utilisateur.")
        return redirect("follows")
    # add the follower to the blocks list
    user.blocks.add(user_to_block)
    # removed from the blocked user's following
    user_to_block.follows.remove(user)
    # if followed, unfollow the blocked user
    if user_to_block in user.follows.all():
        user.follows.remove(user_to_block)
    messages.success(request, f"Vous avez bloqué {user_to_block.username}.")
    return redirect("follows")


@login_required
def unblock_user(request, user_id):
    """Unblock a blocked user"""
    user_to_unblock = get_object_or_404(User, id=user_id)
    user = request.user
    if user_to_unblock in user.blocks.all():
        user.blocks.remove(user_to_unblock)
        # add back the user to the blocked user's following
        user_to_unblock.follows.add(user)
        messages.success(request, f"Vous avez débloqué {user_to_unblock.username}.")
    return redirect("follows")
