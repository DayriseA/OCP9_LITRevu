from django import template
from django.utils import timezone

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR

register = template.Library()


@register.simple_tag(takes_context=True)
def author_display(context, user):
    """If current user is the author, display "vous" instead of the username."""
    if context["user"] == user:
        return "vous"
    return user.username


@register.filter
def post_time_display(post_time):
    """
    Displays the time elapsed since the post was created,
    or the date if it's older than a day.
    """
    seconds_ago = (timezone.now() - post_time).total_seconds()
    if seconds_ago <= HOUR:
        return f"il y a {int(seconds_ago // MINUTE)}min."
    elif seconds_ago <= DAY:
        return f"il y a {int(seconds_ago // HOUR)}h."
    else:
        return f"{post_time.strftime('%H:%M, %d %B %Y')}"
