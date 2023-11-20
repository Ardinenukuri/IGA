"""
leave/apps.py - Application configuration for the 'leave' app.

This module defines the configuration for the 'leave' app.
"""

from django.apps import AppConfig

class LeaveConfig(AppConfig):
    """
    AppConfig class for the 'leave' app.

    Configures the 'leave' app with default_auto_field and app name.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'leave'
