from django.conf import settings
from django.utils import translation


class LocaleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        locale = translation.get_language_from_request(request)
        if locale not in dict(settings.LANGUAGES).keys():
            locale = settings.LANGUAGE_CODE

        translation.activate(locale)
        request.LANGUAGE_CODE = translation.get_language()

        response = self.get_response(request)
        translation.deactivate()

        return response
