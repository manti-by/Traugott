import json
import logging
from django.http import JsonResponse

from shots.models import Shot, ShotType

logger = logging.getLogger('app')


def shots_add(request):
    try:
        data = json.loads(request.body)
        if not len(data):
            return JsonResponse({'status': 204,
                                 'message': 'Data is empty'}, status=200)
        for item in data:
            if item['quantity'] > 0:
                shot = Shot(user=request.user,
                            type=ShotType.objects.get(id=item['type']),
                            quantity=item['quantity'])
                shot.save()
        user_types, all_types = ShotType.objects.get_splitted_for_user(request.user)
        # @todo: add handlebars renderer for shot types
        return JsonResponse({'status': 200,
                             'data': {
                                 'shots': Shot.objects.get_for_response(request.user),
                                 'user_types': user_types,
                                 'all_types': all_types
                             }}, status=200)
    except Exception as e:
        return JsonResponse({'status': 500,
                             'message': e}, status=200)


def shots_update(request):
    try:
        data = json.loads(request.body)
        if not data['id']:
            return JsonResponse({'status': 204,
                                 'message': 'Data is empty'}, status=200)

        shot = Shot.objects.get(id=data['id'], user=request.user)
        shot.quantity = data['quantity']
        shot.save()
        return JsonResponse({'status': 200,
                             'data': shot.as_dict()}, status=200)
    except Shot.DoesNotExist as e:
        logger.warning(e)
        return JsonResponse({'status': 404,
                             'message': e}, status=200)
    except Exception as e:
        logger.error(e)
        return JsonResponse({'status': 500,
                             'message': e}, status=200)


def shots_delete(request):
    try:
        data = json.loads(request.body)
        if not data['id']:
            return JsonResponse({'status': 204,
                                 'message': 'Data is empty'}, status=200)

        shot = Shot.objects.get(id=data['id'], user=request.user)
        shot.deleted = 1
        shot.save()
        return JsonResponse({'status': 200}, status=200)
    except Shot.DoesNotExist as e:
        logger.warning(e)
        return JsonResponse({'status': 404,
                             'message': e}, status=200)
    except Exception as e:
        logger.error(e)
        return JsonResponse({'status': 500,
                             'message': e}, status=200)
