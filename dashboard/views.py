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

    participations_url = "http://127.0.0.1:{}/tuning/v1/participations".format(request.META.get("SERVER_PORT"))
    participations_response = requests.get(participations_url)

    if competition_response.ok and participations_response.ok:
      competition = json.loads(competition_response.content.decode("utf-8"))["data"]
      participations = json.loads(participations_response.content.decode("utf-8"))["data"]
      context = {"success": True, "competition": competition, "participations": participations}

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
def v1_participation(request, competition_id):
  if request.method == "GET":
    competition_url = "http://127.0.0.1:{}/tuning/v1/competitions/{}".format(
            request.META.get("SERVER_PORT"), competition_id)
    competition_response = requests.get(competition_url)

    participations_url = "http://127.0.0.1:{}/tuning/v1/participations".format(request.META.get("SERVER_PORT"))
    participations_response = requests.get(participations_url)

    if competition_response.ok and participations_response.ok:
      competition = json.loads(competition_response.content.decode("utf-8"))["data"]
      participations = json.loads(participations_response.content.decode("utf-8"))["data"]
      context = {"success": True, "competition": competition, "participations": participations}
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
def v1_study_suggestions(request, study_id):
  if request.method == "POST":
    trials_number_string = request.POST.get("trials_number", "1")
    trials_number = int(trials_number_string)

    data = {"trials_number": trials_number}
    url = "http://127.0.0.1:{}/suggestion/v1/studies/{}/suggestions".format(
        request.META.get("SERVER_PORT"), study_id)
    response = requests.post(url, json=data)
    messages.info(request, response.content)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
  else:
    return JsonResponse({"error": "Unsupported http method"})


@csrf_exempt
def v1_trials(request):
  if request.method == "POST":
    study_id = request.POST.get("study_id", "")
    name = request.POST.get("name", "")

    data = {"name": name}

    url = "http://127.0.0.1:{}/suggestion/v1/studies/{}/trials".format(
        request.META.get("SERVER_PORT"), study_id)
    response = requests.post(url, json=data)
    messages.info(request, response.content)
    return redirect("index")
  else:
    return JsonResponse({"error": "Unsupported http method"})


@csrf_exempt
def v1_trial(request, study_id, trial_id):
  url = "http://127.0.0.1:{}/suggestion/v1/studies/{}/trials/{}".format(
      request.META.get("SERVER_PORT"), study_id, trial_id)

  if request.method == "GET":
    response = requests.get(url)

    tiral_metrics_url = "http://127.0.0.1:{}/suggestion/v1/studies/{}/trials/{}/metrics".format(
        request.META.get("SERVER_PORT"), study_id, trial_id)
    tiral_metrics_response = requests.get(tiral_metrics_url)

    if response.ok and tiral_metrics_response.ok:
      trial = json.loads(response.content.decode("utf-8"))["data"]
      trial_metrics = json.loads(
          tiral_metrics_response.content.decode("utf-8"))["data"]
      context = {
          "success": True,
          "trial": trial,
          "trial_metrics": trial_metrics
      }
      return render(request, "paticipation_detail.html", context)
    else:
      response = {
          "error": True,
          "message": "Fail to request the url: {}".format(url)
      }
      return JsonResponse(response, status=405)
  elif request.method == "DELETE":
    response = requests.delete(url)
    messages.info(request, response.content)
    return redirect("index")
  elif request.method == "PUT" or request.method == "POST":
    objective_value_string = request.POST.get("objective_value", "1.0")
    objective_value = float(objective_value_string)
    status = request.POST.get("status", "Completed")
    data = {"objective_value": objective_value, "status": status}
    response = requests.put(url, json=data)
    messages.info(request, response.content)

    trial = json.loads(response.content.decode("utf-8"))["data"]
    context = {"success": True, "trial": trial, "trial_metrics": []}
    return render(request, "participation_detail.html", context)
  else:
    response = {
        "error": True,
        "message": "{} method not allowed".format(request.method)
    }
    return JsonResponse(response, status=405)


@csrf_exempt
def v1_study_trial_metrics(request, study_id, trial_id):
  if request.method == "POST":
    training_step_string = request.POST.get("training_step", "1")
    training_step = int(training_step_string)
    objective_value_string = request.POST.get("objective_value", "1.0")
    objective_value = float(objective_value_string)

    data = {"training_step": training_step, "objective_value": objective_value}
    url = "http://127.0.0.1:{}/suggestion/v1/studies/{}/trials/{}/metrics".format(
        request.META.get("SERVER_PORT"), study_id, trial_id)
    response = requests.post(url, json=data)
    messages.info(request, response.content)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
  else:
    return JsonResponse({"error": "Unsupported http method"})


@csrf_exempt
def v1_study_trial_metric(request, study_id, trial_id, metric_id):
  url = "http://127.0.0.1:{}/suggestion/v1/studies/{}/trials/{}/metrics/{}".format(
      request.META.get("SERVER_PORT"), study_id, trial_id, metric_id)

  if request.method == "GET":
    response = requests.get(url)

    if response.ok:
      trial_metric = json.loads(response.content.decode("utf-8"))["data"]
      context = {"success": True, "trial_metric": trial_metric}
      # TODO: Add the detail page of trial metric
      return render(request, "participation_detail.html", context)
    else:
      response = {
          "error": True,
          "message": "Fail to request the url: {}".format(url)
      }
      return JsonResponse(response, status=405)
  elif request.method == "DELETE" or request.method == "POST":
    response = requests.delete(url)
    messages.info(request, response.content)
    return redirect("index")
  else:
    response = {
        "error": True,
        "message": "{} method not allowed".format(request.method)
    }
    return JsonResponse(response, status=405)
