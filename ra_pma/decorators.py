from django.core.exceptions import PermissionDenied
from functools import wraps


def ra_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_profile = getattr(request.user, 'userprofile', None)
        if user_profile.is_RA:
            return view_func(request, *args, **kwargs)
        raise PermissionDenied  # 403

    return _wrapped_view


def restrict_roles(disallowed_roles, redirect_to='ra_dashboard'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user_profile = getattr(request.user, 'userprofile', None)
            if user_profile:
                if user_profile.is_RA and 'ra' in disallowed_roles:
                    raise PermissionDenied  # 403
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
