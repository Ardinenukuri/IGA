from django import forms
from leave.models import LeaveApplication

class LeaveApplicationForm(forms.ModelForm):
    """
    Form for Leave Applications.

    This form is used for submitting leave applications and includes fields for
    start date, end date, and reason.
    """

    class Meta:
        model = LeaveApplication
        fields = ['start_date', 'end_date', 'reason']

    def custom_validation(self):
        """
        Perform custom validation.

        This method can be used to add custom validation logic beyond what
        is provided by the built-in form validation.
        """
        # Your custom validation logic goes here

class LeaveApprovalForm(forms.ModelForm):
    """
    Form for Leave Approval.

    This form is used for approving or rejecting leave applications and includes a
    field for the approval status.
    """

    class Meta:
        model = LeaveApplication
        fields = ['status']
        # You can customize the widget or add validation if needed
    # For example, you might want to limit the choices for the status field:
    STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.RadioSelect)
