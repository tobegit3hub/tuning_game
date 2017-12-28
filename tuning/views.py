# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


import json

from django.shortcuts import render
from django.http import JsonResponse
from django.http import QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db import IntegrityError, transaction

from tuning.models import Competition
from tuning.models import Participation
from tuning.models import Trial



def index(request):
    response = {"message": "Welcome to tuning game"}
    return JsonResponse(response)


def v1_participations(request):
    response = {"message": "Welcome to tuning game"}
    return JsonResponse(response)

def v1_participation(request):
    response = {"message": "Welcome to tuning game"}
    return JsonResponse(response)

def v1_trials(request):
    response = {"message": "Welcome to tuning game"}
    return JsonResponse(response)

def v1_trial(request):
    response = {"message": "Welcome to tuning game"}
    return JsonResponse(response)
