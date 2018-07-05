from django.views import generic
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import random
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse
from django.shortcuts import render
from chatbot_tutorial.models import RequestCounts
from django.db.models import F


def chat(request):
    context = {}
    return render(request, 'chatbot_tutorial/chatbot.html', context)

"""method for rendering the list of request counts"""
def list(request):
    context = {'data':RequestCounts.objects.all()}
    return render(request, 'chatbot_tutorial/list.html', context)


def respond_to_websockets(message):
    jokes = {
     'stupid': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""",
                """Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""],
     'fat':    ["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""",
                """ Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """],
     'dumb':   ["""Yo' Mama is so dumb, when God was giving out brains, she thought they were milkshakes and asked for extra thick.""",
                """Yo' Mama is so dumb, she locked her keys inside her motorcycle."""]
     }

    result_message = {
        'type': 'text'
    }
    if 'fat' in message['text']:
        result_message['text'] = random.choice(jokes['fat'])

        result = RequestCounts.objects.filter(username = message['username'])
        if result:
            RequestCounts.objects.filter(username = message['username']).update(fat=F('fat')+1)
        else:
            RequestCounts(username = message['username'], fat = 1, stupid = 0, dump = 0).save()


    elif 'stupid' in message['text']:
        result_message['text'] = random.choice(jokes['stupid'])
        result = RequestCounts.objects.filter(username = message['username'])
        if result:
            RequestCounts.objects.filter(username = message['username']).update(stupid=F('stupid')+1)
        else:
            RequestCounts(username = message['username'], fat = 0, stupid = 1, dump = 0).save()

    elif 'dumb' in message['text']:
        result_message['text'] = random.choice(jokes['dumb'])
        result = RequestCounts.objects.filter(username = message['username'])
        if result:
            RequestCounts.objects.filter(username = message['username']).update(dump=F('dump')+1)
        else:
            RequestCounts(username = message['username'], fat = 0, stupid = 0, dump = 1).save()

    elif message['text'] in ['hi', 'hey', 'hello']:
        result_message['text'] = "Hello to you too! If you're interested in yo mama jokes, just tell me fat, stupid or dumb and i'll tell you an appropriate joke."
    else:
        result_message['text'] = "I don't know any responses for that. If you're interested in yo mama jokes tell me fat, stupid or dumb."

    return result_message
