import logging
from django.shortcuts import render_to_response
from django.http import Http404


logger = logging.getLogger('app')


def index(request):
    try:
        return render_to_response('index.html')
    except Exception as e:
        logger.exception(e)
        raise Http404