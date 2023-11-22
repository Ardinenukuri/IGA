"""
leave/views.py - Module for handling views related to leave management.

This module contains views for leave-related functionality, including leave application
submission, status checking, and approval.
"""

from django.db import models
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from leave.models import LeaveApplication
from leave.forms import LeaveApplicationForm, LeaveApprovalForm
from django.shortcuts import get_object_or_404

# Explicitly add the default manager to the LeaveApplication model
LeaveApplication.objects = models.Manager()

@login_required
def create_leave_application(request):
    """
    View function for creating a leave application.

    If the request method is POST, processes the submitted form data.
    If the form is valid, saves the leave application and redirects to the leave list.
    If the request method is GET, renders the leave application form.
    """
    if request.method == 'POST':
        form = LeaveApplicationForm(request.POST)
        if form.is_valid():
            leave_application = form.save(commit=False)
            leave_application.requested_by = request.user
            leave_application.save()
            return redirect('leave:leave_list')
    else:
        form = LeaveApplicationForm()
    return render(
        request,
        'leave/create_leave_application.html',
        {'form': form}
    )

@login_required
def leave_list(request):
    """
    View function for displaying the list of leave applications for the logged-in user.
    """
    leave_applications = LeaveApplication.objects.filter(requested_by=request.user)
    return render(
        request,
        'leave/leave_list.html',
        {'leave_applications': leave_applications}
    )

@staff_member_required
def leave_approval(request, leave_id):
    """
    View function for approving or rejecting a leave application.

    If the request method is POST, processes the submitted form data.
    If the form is valid, updates the leave application status and redirects to the leave list.
    If the request method is GET, renders the leave approval form.
    """
    leave_application = get_object_or_404(LeaveApplication, pk=leave_id)

    if request.method == 'POST':
        form = LeaveApprovalForm(request.POST, instance=leave_application)
        if form.is_valid():
            # Save the form directly to update the instance
            form.save()
            return redirect('leave:leave_list')
    else:
        form = LeaveApprovalForm(instance=leave_application)

    return render(
        request,
        'leave/leave_approval.html',
        {'form': form, 'leave_application': leave_application}
    )