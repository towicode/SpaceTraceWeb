from django.http import JsonResponse, HttpResponseBadRequest
from spaceSession.models import *
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.http import HttpResponse
import json


def viewSession(request, id):
    """ Display the home page """

    template = loader.get_template('spaceSession/view.html')
    context = {}
    return HttpResponse(template.render(context, request))

def index(request):
    """ Display the home page """

    template = loader.get_template('spaceSession/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def pageUpdates(request, id):
    """ Handles all ccommunications between Web View and Django"""

    #   First we get the current session requested and the 
    #   Step Number
    my_session = SpaceSession.objects.get(pk=id)
    step = 1

    if (my_session.step_one.completed):
        if (my_session.step_two.completed):
            if (my_session.step_three.completed):
                if (my_session.step_four.completed):
                    step = 5
                else:
                    step = 4         
            else:
                step = 3
        else:
            step = 2
    
    #   Next we determine if it is a GET or a POST
    #   and send it off to helper functions

    if (request.method == 'POST'):
        return page_update_post(request, step, my_session)
    elif (request.method == 'GET'):
        return page_update_get(request, step, my_session)

def page_update_get(request, step, my_session):
    """ handles all get requests for page_updates """

    if (step == 1):
        return JsonResponse({"step": 1})

    if (step == 2):
        return JsonResponse({"step": 2})

    if (step == 3):
        b = {
            "step": 3,
            "image": my_session.step_three.data['image'],
            "label": my_session.step_three.data['label'],
            "info": my_session.step_three.data['info'],
        }
        return JsonResponse(b)
        

def page_update_post(request, step, my_session):
    """ Handes all post requests for page_update """
    #   Step one the users posts the files to upload
    request_body = json.loads(request.body)
    if (step == 1):
        if ("files_to_upload" not in request_body or "arguments" not in request_body ):
            return HttpResponseBadRequest("Invalid page_update_post step1")
        #   update step2 and complete step1
        dog = json.dumps(dict(request.POST))
        my_session.step_two.arguments = request_body['arguments']
        my_session.step_two.files_to_upload = request_body['files_to_upload']
        my_session.step_two.save()

        my_session.step_one.completed = True
        my_session.step_one.save()

        return JsonResponse({"valid": "ok"})

    elif (step == 3):
        if ("data" not in request_body):
            return HttpResponseBadRequest("Invalid page_update_post step3")
        
        # update step4 and complete step3
        my_session.step_four.data = request_body['data']
        my_session.step_four.save()

        my_session.step_three.completed = True
        my_session.step_three.save()

        return JsonResponse({"valid": "ok"})




@csrf_exempt
def spaceSessionHelper(request, id):
    """ Handles all requests between SpaceTraceWeb and SpaceTraceHPC """

    my_session = SpaceSession.objects.get(pk=id)

    step = 1

    if (my_session.step_one.completed):
        if (my_session.step_two.completed):
            if (my_session.step_three.completed):
                if (my_session.step_four.completed):
                    step = 5
                else:
                    step = 4         
            else:
                step = 3
        else:
            step = 2
    
    if (request.method == 'POST'):
        return helper_post(request, my_session)
    elif (request.method == 'GET'):
        return helper_get(request, step, my_session)

    return HttpResponseBadRequest("Invalid Method")


def helper_post(request, my_session):
    """ helper function to determine post instructions

    Specifically if post is supposed to be step one or step three"""

    request_body = json.loads(request.body)


    if ("image" in request_body):
        return step_three_helper(request_body, my_session)
    elif("finish_instructions" in request_body):
        return step_five_heler(request_body, my_session)

def helper_get(request, step, my_session):
    """ helper function to detemine get instructions

    specfically to help direct which info to display 
    on a get request depending on which step the current
    session is at"""

    if (step == 1):
        return JsonResponse({'step' : 1})

    elif (step == 2):
        b = {
            'step' : 2,
            'files_to_upload' : my_session.step_two.files_to_upload,
            'arguments' : my_session.step_two.arguments
        }

        return JsonResponse(b)

    elif (step == 3):
        return JsonResponse({'step' : 3})

    elif (step == 4):
        b = {
            'step': 4,
            'data': my_session.step_four.data
        }
        return JsonResponse(b)

    return HttpResponseBadRequest("Invalid get")



def step_three_helper(request_body, my_session):
    """ Step three post function

    sets the image, label, and info paramaters for
    step three """

    if ("image" not in request_body or "label" not in request_body or "info" not in request_body):
        return HttpResponseBadRequest("Invalid step three post")

    b = {
        'image': request_body['image'],
        'label': request_body['label'],
        'info': request_body['info']
    }
    my_session.step_two.completed = True
    my_session.step_two.save()

    my_session.step_three.data = b
    my_session.step_three.save()

    return JsonResponse({"valid": "ok"})


def step_five_heler(request_body, my_session):
    """ step five post function

    sets the finish instructions per after the job
    is absolutely complete """

    if ("finish_instructions" not in request_body):
        return HttpResponseBadRequest("Invalid step three post")
    
    b = {
        'finish_instructions' : request_body['finish_instructions']
    }

    my_session.step_four.completed = True
    my_session.step_four.save()

    my_session.step_five.data = b
    my_session.step_five.save()

    return JsonResponse({"valid": "ok"})



@csrf_exempt
def spaceSessionCreate(request):
    """ Creates a spaceSession """

    if (request.method == 'GET'):
        objs = SpaceSession.objects.filter(step_four__completed=False)
        b = []
        for obj in objs:
            c = {
                'id': obj.pk,
                'date': obj.created
            }
            b.append(c)
        return JsonResponse({'list' : b})


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

    try:
        f = step_five()
        f.save()
        new_session.step_five = f
    except Exception as e:
        print(e)

    new_session.save()
    return JsonResponse({'sessionId': new_session.pk})
