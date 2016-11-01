import logging

from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.templatetags.staticfiles import static as static_file

from traugott.utils import random_date

logger = logging.getLogger('app')


@login_required
def home_page(request):
    try:
        shots = []
        user = request.user.profiles.as_dict()
        for i in range(0, 10):
            shots.append({
                'date': random_date(),
                'text': '500ml',
                'image': static_file('img/beer.jpg')
            })
        return render(request, 'index.html', {'user': user, 'shots': shots})
    except Exception as e:
        logger.exception(e)
        raise Http404


def static_page(request, page):
    try:
        return render(request,'static/%s.html' % page,
                      {'user': request.user.profiles.as_dict()})
    except Exception as e:
        logger.exception(e)
        raise Http404

