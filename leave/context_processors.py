"""
leave/context_processors.py - Context processors for leave-related functionality.

This module defines context processors, including one for retrieving upcoming leaves.
"""

from django.utils import timezone
from .models import LeaveApplication

# pylint: disable=no-member
def upcoming_leaves(request):
    """
    Context processor to retrieve upcoming leaves.

    Returns a dictionary with the 'upcoming_leaves' key and a queryset of upcoming leave
    applications as the corresponding value.
    """
    upcoming_leaves = None

    user = request.user
    if user.is_authenticated:
        one_week_from_now = timezone.now() + timezone.timedelta(days=7)
        upcoming_leaves = LeaveApplication.objects.filter(
            # requested_by=user,
            # start_date__gt=timezone.now().date(),
            # start_date__lte=one_week_from_now.date()
        )
    return {'upcoming_leaves': upcoming_leaves}
