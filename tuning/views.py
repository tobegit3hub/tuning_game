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


@csrf_exempt
def v1_trial_execute(request, trial_id):

  if request.method == "POST":
    trial = Trial.objects.get(id=trial_id)

    #from competition.return_input_game import ReturnInputGame
    #competition = ReturnInputGame()
    from competition.square_function import SquareFunction
    competition = SquareFunction()
    metrics = competition.execute(trial.parameters_instance)

    trial.metrics = metrics
    trial.save()

    return JsonResponse({"data": trial.to_json()})

  else:
    return JsonResponse({"error": "Unsupported http method"})
