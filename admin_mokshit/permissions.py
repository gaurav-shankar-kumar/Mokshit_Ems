from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from django.core.exceptions import PermissionDenied



def administration_permission_required(login_url=None, raise_exception=False):
    """
    Decorator for views that checks whether a user has a particular permission
    enabled, redirecting to the log-in page if necessary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """

    def check_perms(user):
        
        if user.is_authenticated:
            if user.is_superuser or user.is_admin :
                return True
            else:
            # messages.error(request,'Permission Denied')
                raise PermissionDenied
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False

    return user_passes_test(check_perms, login_url=login_url)