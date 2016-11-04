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

        user_shot_types = []
        user_shot_types_ids = []
        for shot_type in ShotType.objects.get_for_user(request.user):
            user_shot_types.append(shot_type.as_dict())
            user_shot_types_ids.append(shot_type.id)

        all_shot_types = []
        for shot_type in ShotType.objects.exclude(id__in=user_shot_types_ids):
            all_shot_types.append(shot_type.as_dict())

        return render(request, 'index.html', {'user': user, 'shots': shots,
                                              'user_shot_types': user_shot_types,
                                              'all_shot_types': all_shot_types })
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

