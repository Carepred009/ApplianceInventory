# mixins.py
from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import redirect


class GroupRequiredMixin(AccessMixin):
    """
    Verify that the current user is in the required group.
    Usage:
        class MyView(GroupRequiredMixin, View):
            group_required = 'Supervisor'
    """
    group_required = None  # can be a string or a list/tuple of group names

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        # Convert to tuple if single string
        groups = self.group_required
        if isinstance(groups, str):
            groups = (groups,)

        # Check if user is in any of the required groups
        if not request.user.groups.filter(name__in=groups).exists():
            raise PermissionDenied  # or redirect to a 'no permission' page
            # show message and redirect
           # messages.error(request, "You do not have permission to access this page.")
            #return redirect('home')  # or any page you want

        return super().dispatch(request, *args, **kwargs)
