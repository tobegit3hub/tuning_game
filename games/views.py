# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import IntegrityError, transaction
from django.http import JsonResponse, QueryDict
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from tuning.models import Competition, Participation, Trial


#  TODO: Setup the page to choose game and Partition
def index(request):
  response = {"message": "Welcome to tuning game"}
  return JsonResponse(response)


def play(request):

  if request.method == "GET":

    competition_name = "OneUnknowQuadraticEquation"
    competition = Competition.objects.get(name=competition_name)

    participations = Participation.objects.filter(competition=competition)

    username = "wawa"
    participation = Participation.objects.get(
        competition=competition, username=username)

    trials = Trial.objects.filter(participation=participation)

    context = {
        "success": True,
        "competition": competition,
        "participations": participations,
        "participation": participation,
        "trials": trials
    }
    return render(request, "phaser_tutorial/index.html", context)

  else:
    response = {
        "error": True,
        "message": "{} method not allowed".format(request.method)
    }
    return JsonResponse(response, status=405)
