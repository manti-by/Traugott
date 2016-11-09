from django.conf import settings


def django_conf(request):
    return {'USE_COMPRESSOR': settings.USE_COMPRESSOR}
