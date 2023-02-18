from django.middleware.security import SecurityMiddleware
from django.http import HttpResponsePermanentRedirect
from django.conf import settings


class ExtSecurityMiddleware(SecurityMiddleware):
    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.redirect_reverse = settings.SECURE_REDIRECT_REVERSE

    def process_request(self, request):
        process = super().process_request(request)
        if process is not None:
            return process
        if self.redirect and request.is_secure() and self.redirect_reverse:
            return self.reverse_process(request)

    def reverse_process(self, request):
        """Utility method"""
        path = request.path.lstrip('/')
        if any(pattern.search(path) for pattern in self.redirect_exempt):
            return HttpResponsePermanentRedirect(
                "http://%s%s" % (request.get_host(), request.get_full_path())
            )
