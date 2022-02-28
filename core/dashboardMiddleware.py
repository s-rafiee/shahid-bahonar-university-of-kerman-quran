from django.shortcuts import redirect, reverse


class DashboardMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/dashboard/'):
            if not request.user.is_authenticated:
                return redirect(reverse('login_page'))
            if request.user.completed is False and not request.path.startswith(
                    '/dashboard/profile/') and not request.path.startswith('/dashboard/logout/'):
                return redirect(reverse('dashboard_profile'))
        response = self.get_response(request)
        return response
