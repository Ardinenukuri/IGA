from django.http import HttpResponseForbidden
from django.utils import timezone
from leave.models import LeaveApplication

class LeaveMiddleware:
    """
    Middleware class for handling leave-related functionality.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            current_date = timezone.now().date()
            on_leave = False # LeaveApplication.objects.filter(
                # requested_by=user,
                # start_date__lte=current_date,
                # end_date__gte=current_date,
                # status='approved'
            # ).exists()

            if on_leave:
                return HttpResponseForbidden("You are on leave. Access denied.")
            
        response = self.get_response(request)
        return response

   