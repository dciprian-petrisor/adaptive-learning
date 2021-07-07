from django.contrib.auth import authenticate
class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # inject token from cookie if not in headers; used for media retrieval with img tags
        if not hasattr(request.META, 'HTTP_AUTHORIZATION'):
            cookie_token = request.COOKIES.get('token', None)
            if cookie_token:
                request.META['HTTP_AUTHORIZATION'] = f'JWT {cookie_token}'

        user = authenticate(request)
        if user:
            request.user = user
    

        response = self.get_response(request)
        return response