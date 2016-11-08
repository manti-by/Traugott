import logging

from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from shots.models import Shot, ShotType

logger = logging.getLogger('app')


@login_required
def home_page(request):
    try:
        user = request.user.profiles.as_dict()
        shots = Shot.objects.get_for_response(request.user)
        user_types, all_types = ShotType.objects.get_splitted_for_user(request.user)
        return render(request, 'index.html', {'user': user, 'shots': shots,
                                              'user_types': user_types,
                                              'all_types': all_types })
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

