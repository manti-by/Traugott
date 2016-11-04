import json
from django.http import JsonResponse

from shots.models import Shot, ShotType


def shots_add(request):
    try:
        data = json.loads(request.body)
        if not len(data):
            return JsonResponse({'status': 204,
                                 'message': 'Data is empty'}, status=200)

        for item in data:
            if item['quantity'] > 0:
                shot = Shot(user=request.user,
                            type=ShotType.objects.get(id=item['type']))
                shot.save()
        return JsonResponse({'status': 200,
                             'data': Shot.objects.get_for_response(request.user)}, status=200)
    except Exception as e:
        return JsonResponse({'status': 500,
                             'message': e}, status=200)