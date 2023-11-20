"""
leave/urls.py - URL patterns for leave-related views.

This module defines the URL patterns for leave-related functionality, including
leave application submission, status checking, and approval.
"""

from django.urls import path
from leave.views import create_leave_application, leave_list, leave_approval

APP_NAME = 'leave'

urlpatterns = [
    path('create/', create_leave_application, name='create_leave_application'),
    path('list/', leave_list, name='leave_list'),
    path('approval/<int:leave_id>/', leave_approval, name='leave_approval'),
]
