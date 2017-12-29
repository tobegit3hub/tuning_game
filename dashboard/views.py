# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import platform

import requests
from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import (Http404, HttpResponse, HttpResponseRedirect,
                         JsonResponse)
from django.shortcuts import (get_object_or_404, redirect, render,
                              render_to_response)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from tuning.models import Competition, Participation, Trial


def home(request):
  pass


def index(request):
  try:
    competitions = [competition for competition in Competition.objects.all()]
  except Competition.DoesNotExist:
    competitions = []

  try:
    participations = [
        participation for participation in Participation.objects.all()
    ]
  except Participation.DoesNotExist:
    participations = []

  try:
    trials = [trial for trial in Trial.objects.all()]
  except Trial.DoesNotExist:
    trials = []

  context = {
      "success": True,
      "competitions": competitions,
      "participations": participations,
      "trials": trials
  }
  return render(request, "index.html", context)


@csrf_exempt
def v1_competition(request, competition_id):
  if request.method == "GET":
    competition_url = "http://127.0.0.1:{}/tuning/v1/competitions/{}".format(
        request.META.get("SERVER_PORT"), competition_id)
    competition_response = requests.get(competition_url)

    participations_url = "http://127.0.0.1:{}/tuning/v1/participations?competition_id={}".format(
        request.META.get("SERVER_PORT"), competition_id)
    participations_response = requests.get(participations_url)

    if competition_response.ok and participations_response.ok:
      competition = json.loads(
          competition_response.content.decode("utf-8"))["data"]
      participations = json.loads(
          participations_response.content.decode("utf-8"))["data"]
      context = {
          "success": True,
          "competition": competition,
          "participations": participations
      }

      return render(request, "competition_detail.html", context)
    else:
      response = {"error": True, "message": "Fail to request the resources"}
      return JsonResponse(response, status=405)
  else:
    response = {
        "error": True,
        "message": "{} method not allowed".format(request.method)
    }
    return JsonResponse(response, status=405)


@csrf_exempt
def v1_participation(request, participation_id):
  if request.method == "GET":
    participation_url = "http://127.0.0.1:{}/tuning/v1/participations/{}".format(
        request.META.get("SERVER_PORT"), participation_id)
    participation_response = requests.get(participation_url)

    trials_url = "http://127.0.0.1:{}/tuning/v1/trials?participation_id={}".format(
        request.META.get("SERVER_PORT"), participation_id)
    trials_response = requests.get(trials_url)

    if participation_response.ok and trials_response.ok:
      participation = json.loads(
          participation_response.content.decode("utf-8"))["data"]
      trials = json.loads(trials_response.content.decode("utf-8"))["data"]
      context = {
          "success": True,
          "participation": participation,
          "trials": trials
      }
      return render(request, "participation_detail.html", context)
    else:
      response = {"error": True, "message": "Fail to request the resources"}
      return JsonResponse(response, status=405)
  else:
    response = {
        "error": True,
        "message": "{} method not allowed".format(request.method)
    }
    return JsonResponse(response, status=405)
