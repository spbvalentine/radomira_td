# tdapp/middleware.py

class DisableCSRFOnAPI:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Отключаем CSRF только для API
        if request.path.startswith('/api/'):
            setattr(request, '_dont_enforce_csrf_checks', True)
        return self.get_response(request)