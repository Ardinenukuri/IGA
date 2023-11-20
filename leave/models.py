"""
leave/models.py - Module containing models for leave management.

This module defines the LeaveApplication model for managing leave-related information.
"""

from django.db import models
from django.conf import settings


class LeaveApplication(models.Model):
    """
    Model for Leave Applications.

    Represents a leave application with information such as start date, end date, status,
    requested user, processing user, and reason.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='leave_requests'
    )
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='processed_leaves'
    )
    
    reason = models.TextField()

    def __str__(self):
        """
        String representation of the LeaveApplication.

        Returns a formatted string with the requested user's username.
        """
        return f"{self.requested_by.username}'s Leave Request"
