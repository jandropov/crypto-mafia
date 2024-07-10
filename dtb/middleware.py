def AdminSession(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = get_response(request)
        user = request.user
        if user.is_staff:
            request.session.set_expiry(30*60)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware
