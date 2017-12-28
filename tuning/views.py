# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import importlib
import json

from django.conf import settings
from django.db import IntegrityError, transaction
from django.http import JsonResponse, QueryDict
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from tuning.models import Competition, Participation, Trial


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

    competiton_name_package_map = settings.REGISTERED_COMPETITION

    # module_name = "tuning.competition.square_function"
    # class_name = "SquareFunction"
    class_name = trial.particiption.competition.name
    module_name = competiton_name_package_map.get(class_name)

    module = importlib.import_module(module_name)
    clazz = getattr(module, class_name)
    competition = clazz()

    metrics = competition.execute(trial.parameters_instance)
    trial.metrics = metrics
    trial.save()

    return JsonResponse({"data": trial.to_json()})

  else:
    return JsonResponse({"error": "Unsupported http method"})
