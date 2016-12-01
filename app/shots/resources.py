import json
import logging

from simple_rest import Resource
from django.http import JsonResponse

from shots.models import Shot, ShotType, ShotIcon
from shots.utils import resource_wrapper

logger = logging.getLogger('app')


class ShotResource(Resource):

    @resource_wrapper
    def get(self, request):
        shots = Shot.objects.get_for_response(request.user)
        return JsonResponse({'status': 200,
                             'data': shots}, status=200)

    @resource_wrapper
    def post(self, request):
        data = json.loads(request.body)
        if not len(data):
            return JsonResponse({'status': 204,
                                 'message': 'Data is empty'}, status=200)
        for item in data:
            if item['volume'] > 0:
                shot = Shot(user=request.user,
                            type=ShotType.objects.get(id=item['type']),
                            volume=item['volume'])
                shot.save()
        user_types, all_types = ShotType.objects.get_splitted_for_user(request.user)
        popular = user_types[0]
        del user_types[0]
        return JsonResponse({'status': 200,
                             'data': {
                                 'shots': Shot.objects.get_for_response(request.user),
                                 'popular': popular,
                                 'user_types': user_types,
                                 'all_types': all_types
                             }}, status=200)

    @resource_wrapper
    def patch(self, request):
        data = json.loads(request.body)
        if not data['id']:
            return JsonResponse({'status': 204,
                                 'message': 'Data is empty'}, status=200)

        shot = Shot.objects.get(id=data['id'], user=request.user)
        shot.volume = data['volume']
        shot.save()
        return JsonResponse({'status': 200,
                             'data': shot.as_dict()}, status=200)

    @resource_wrapper
    def delete(self, request):
        data = json.loads(request.body)
        if not data['id']:
            return JsonResponse({'status': 204,
                                 'message': 'Data is empty'}, status=200)

        shot = Shot.objects.get(id=data['id'], user=request.user)
        shot.deleted = 1
        shot.save()
        return JsonResponse({'status': 200}, status=200)


class ShotTypeResource(Resource):

    @staticmethod
    def get_for_user(user):
        user_types, all_types = ShotType.objects.get_splitted_for_user(user)
        popular = all_types[0]
        if len(user_types):
            popular = user_types[0]
            del user_types[0]
        return popular, user_types, all_types

    @resource_wrapper
    def get(self, request):
        popular, user_types, all_types = self.get_for_user(request.user)
        return JsonResponse({'status': 200,
                             'data': {
                                 'popular': popular,
                                 'user_types': user_types,
                                 'all_types': all_types
                             }}, status=200)

    @resource_wrapper
    def post(self, request):
        data = json.loads(request.body)
        if not data['title']:
            return JsonResponse({'status': 204,
                                 'message': 'Data is empty'}, status=200)
        item = ShotType(title=data['title'],
                        volume=data['volume'],
                        degree=data['degree'],
                        cost=data['cost'],
                        user=request.user)
        try:
            item.icon = ShotIcon.objects.get(id=data['icon'])
        except ShotIcon.DoesNotExist:
            pass
        item.save()

        popular, user_types, all_types = self.get_for_user(request.user)
        return JsonResponse({'status': 200,
                             'data': {
                                 'popular': popular,
                                 'user_types': user_types,
                                 'all_types': all_types
                             }}, status=200)

    @resource_wrapper
    def patch(self, request):
        data = json.loads(request.body)
        if not data['id']:
            return JsonResponse({'status': 204,
                                 'message': 'Data is empty'}, status=200)

        item = ShotType.objects.get(id=data['id'], user=request.user)
        item.title = data['title']
        item.volume = data['volume']
        item.degree = data['degree']
        item.save()
        return JsonResponse({'status': 200,
                             'data': item.as_dict()}, status=200)

    @resource_wrapper
    def delete(self, request):
        data = json.loads(request.body)
        if not data['id']:
            return JsonResponse({'status': 204,
                                 'message': 'Data is empty'}, status=200)

        item = ShotType.objects.get(id=data['id'], user=request.user)
        item.deleted = 1
        item.save()
        return JsonResponse({'status': 200}, status=200)


class ShotIconResource(Resource):

    @resource_wrapper
    def get(self, request):
        icons = ShotIcon.objects.get_for_response(request.user)
        return JsonResponse({'status': 200,
                             'data': icons }, status=200)
