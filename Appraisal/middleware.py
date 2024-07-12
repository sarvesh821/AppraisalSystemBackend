# middleware.py
from django.middleware.csrf import get_token
from django.utils.deprecation import MiddlewareMixin

class SetCSRFCookieMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
       
        response['X-CSRFToken'] = get_token(request)
        return response