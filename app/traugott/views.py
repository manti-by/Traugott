import logging

from random import randrange
from datetime import datetime, timedelta

from django.http import Http404, JsonResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

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


@login_required
def index(request):
    try:
        cards = []
        for i in range(0, 10):
            cards.append({
                'date': random_date()
            })
        return render_to_response('index.html', {'cards': cards})
    except Exception as e:
        logger.exception(e)
        raise Http404


def random_date():
    start = datetime.strptime('9/9/2016 1:30 PM', '%m/%d/%Y %I:%M %p')
    end = datetime.strptime('10/10/2016 4:50 AM', '%m/%d/%Y %I:%M %p')
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)
