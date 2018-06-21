from django.http import JsonResponse, HttpResponseBadRequest
from spaceSession.models import *
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def spaceSessionCreate(request):
    """ Creates a spaceSession """

    if (request.method != 'POST'):
        return HttpResponseBadRequest("Invalid Method")

    new_session = SpaceSession()

    try:
        a = step_one()
        a.save()
        new_session.step_one = a
    except Exception as e:
        print(e)

    try:
        b = step_two()
        b.save()
        new_session.step_two = b
    except Exception as e:
        print(e)
    
    try:
        c = step_three()
        c.save()
        new_session.step_three = c
    except Exception as e:
        print(e)

    try:
        d = step_four()
        d.save()
        new_session.step_four = d
    except Exception as e:
        print(e)

    new_session.save()
    return JsonResponse({'sessionId': new_session.pk})
