import logging

from django.http import JsonResponse
from simple_rest import Resource

logger = logging.getLogger('app')


class Rest(Resource):

    def response(self, data):
        if 299 < data['status'] < 500:
            logger.warning(data['message'])
        if data['status'] > 499:
            logger.error(data['message'])
        return JsonResponse({'status': data['status'],
                             'message': data['message']}, status=data['status'])