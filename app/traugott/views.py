import logging

from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from shots.models import Shot

logger = logging.getLogger('app')


@login_required
def home_page(request):
    try:
        shots = []
        user = request.user.profiles.as_dict()
        for shot in Shot.objects.filter(user=request.user):
            shots.append(shot.as_dict())
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

