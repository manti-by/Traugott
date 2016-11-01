import json
import logging

from random import randrange
from datetime import datetime, timedelta

from django.http import Http404, JsonResponse
from django.shortcuts import render_to_response
from django.contrib.staticfiles.templatetags.staticfiles import static

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
                    'image': static('img/beer.jpg')
                })

        return render_to_response('index.html', {'user': json.dumps(user),
                                                 'data': json.dumps(data, default=date_handler)})
    except Exception as e:
        logger.exception(e)
        raise Http404


def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


def random_date():
    start = datetime.strptime('9/9/2016 1:30 PM', '%m/%d/%Y %I:%M %p')
    end = datetime.strptime('10/10/2016 4:50 AM', '%m/%d/%Y %I:%M %p')
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)
