from django.conf import settings
from django.shortcuts import redirect


EXEMPT_URLS = [settings.LOGIN_URL.lstrip('/')]

if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [url.lstrip('/') for url in settings.LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')
        path = request.path_info.lstrip('/')

        password_url = 'password-reset/confirm/'
        url_is_exempt = (path in EXEMPT_URLS or password_url in path)

        if not request.user.is_authenticated:
            if not url_is_exempt:
                requested_url = request.get_full_path()
                request.session['requested_url'] = requested_url
                return redirect(settings.LOGIN_REQUIRED_URL)

