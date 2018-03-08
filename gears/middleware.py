
class FarmMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if request.user.is_authenticated:
            request.farm = request.user.farms.first()
        else:
            request.farm = None

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
