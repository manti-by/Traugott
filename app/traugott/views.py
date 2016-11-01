import logging

from django.http import Http404
from django.shortcuts import render_to_response
from django.contrib.staticfiles.templatetags.staticfiles import static as static_file


from traugott.utils import random_date

logger = logging.getLogger('app')


def index(request):
    try:
        user = {}
        data = []
        if request.user.is_authenticated:
            user = request.user.profiles.as_dict()
            for i in range(0, 10):
                data.append({
                    'date': random_date(),
                    'text': '500ml',
                    'image': static_file('img/beer.jpg')
                })
        return render_to_response('index.html', {'user': user, 'data': data})
    except Exception as e:
        logger.exception(e)
        raise Http404


def static(request, page):
    try:
        return render_to_response('static/%s.html' % page, {'user': request.user.profiles.as_dict()})
    except Exception as e:
        logger.exception(e)
        raise Http404

