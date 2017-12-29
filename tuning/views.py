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


@csrf_exempt
def v1_competitions(request):

  if request.method == "GET":
    competitions = Competition.objects.all()
    response_data = [competition.to_json() for competition in competitions]
    return JsonResponse({"data": response_data})

  elif request.method == "POST":
    data = json.loads(request.body)

    name = data["name"]
    parameters_description = json.dumps(data["parameters_description"])
    goal = data["goal"]
    computation_budge = int(data["computation_budge"])

    competition = Competition.create(name, parameters_description, goal, computation_budge)
    return JsonResponse({"data": competition.to_json()})

  else:
    return JsonResponse({"error": "Unsupported http method"})


@csrf_exempt
def v1_competition(request, competition_id):
  competition = Competition.objects.get(id=competition_id)

  if request.method == "GET":
    return JsonResponse({"data": competition.to_json()})

  elif request.method == "DELETE":
    competition.delete()
    return JsonResponse({"message": "Succeed to delete object"})

  elif request.method == "PUT":
    data = json.loads(request.body)

    if "name" in data:
      competition.name = data["name"]
    if "parameters_description" in data:
      competition.status = data["parameters_description"]
    if "goal" in data:
      competition.status = data["goal"]
    if "computation_budge" in data:
      competition.status = data["computation_budge"]
    if "theoretical_best_metrics" in data:
      competition.status = data["theoretical_best_metrics"]

    competition.save()
    return JsonResponse({"data": competition.to_json()})

  else:
    return JsonResponse({"error": "Unsupported http method"})


@csrf_exempt
def v1_participations(request):

  if request.method == "GET":

    competition_id = request.GET.get("competition_id", None)
    if competition_id:
      competition = Competition.objects.get(id=competition_id)
      participations = Participation.objects.filter(competition=competition)
    else:
      participations = Participation.objects.all()

    response_data = [
        participation.to_json() for participation in participations
    ]
    return JsonResponse({"data": response_data})

  elif request.method == "POST":
    data = json.loads(request.body)

    competition_id = data["competition_id"]
    competition = Competition.objects.get(id=competition_id)
    username = data["username"]
    email = data["email"]

    participation = Participation.create(competition, username, email)
    return JsonResponse({"data": participation.to_json()})

  else:
    return JsonResponse({"error": "Unsupported http method"})


@csrf_exempt
def v1_participation(request, participation_id):
  participation = Participation.objects.get(id=participation_id)

  if request.method == "GET":
    return JsonResponse({"data": participation.to_json()})

  elif request.method == "DELETE":
    participation.delete()
    return JsonResponse({"message": "Succeed to delete object"})

  elif request.method == "PUT":
    data = json.loads(request.body)

    if "username" in data:
      participation.username = data["username"]
    if "email" in data:
      participation.email = data["email"]

    participation.save()
    return JsonResponse({"data": participation.to_json()})

  else:
    return JsonResponse({"error": "Unsupported http method"})


@csrf_exempt
def v1_trials(request):

  if request.method == "GET":

    participation_id = request.GET.get("participation_id", None)
    if participation_id:
      participation = Participation.objects.get(id=participation_id)
      trials = Trial.objects.filter(participation=participation)
    else:
      trials = Trial.objects.all()

    response_data = [trial.to_json() for trial in trials]
    return JsonResponse({"data": response_data})

  elif request.method == "POST":
    data = json.loads(request.body)

    particiption_id = data["particiption_id"]
    particiption = Participation.objects.get(id=particiption_id)
    parameters_instance = json.dumps(data["parameters_instance"])

    trial = Trial.create(particiption, parameters_instance)
    return JsonResponse({"data": trial.to_json()})

  else:
    return JsonResponse({"error": "Unsupported http method"})


@csrf_exempt
def v1_trial(request, trial_id):
  trial = Trial.objects.get(id=trial_id)

  if request.method == "GET":
    return JsonResponse({"data": trial.to_json()})

  elif request.method == "DELETE":
    trial.delete()
    return JsonResponse({"message": "Succeed to delete trial"})

  elif request.method == "PUT":
    data = json.loads(request.body)

    if "parameters_instance" in data:
      trial.parameters_instance = data["parameters_instance"]
    if "status" in data:
      trial.status = data["status"]

    trial.save()
    return JsonResponse({"data": trial.to_json()})

  else:
    return JsonResponse({"error": "Unsupported http method"})


@csrf_exempt
def v1_trial_execute(request, trial_id):

  if request.method == "POST":
    trial = Trial.objects.get(id=trial_id)

    # Get competition package by name
    competiton_name_package_map = settings.REGISTERED_COMPETITION
    # Example: "SquareFunction"
    class_name = trial.particiption.competition.name
    # Example: "tuning.competition.square_function"
    module_name = competiton_name_package_map.get(class_name)

    # Dynamically construct competition object
    module = importlib.import_module(module_name)
    clazz = getattr(module, class_name)
    competition = clazz()

    # Run competition to get metrics
    metrics = competition.execute(trial.parameters_instance)

    # Update the trial in database
    trial.metrics = metrics
    trial.save()

    return JsonResponse({"data": trial.to_json()})

  else:
    return JsonResponse({"error": "Unsupported http method"})
