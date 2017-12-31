# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Competition(models.Model):
  name = models.CharField(max_length=128, blank=False)
  parameters_description = models.CharField(max_length=1024, blank=False)
  goal = models.CharField(max_length=128, blank=False, default="MAXIMIZE")
  computation_budge = models.IntegerField(blank=False)
  theoretical_best_metrics = models.FloatField(blank=True, null=True)

  current_best_metrics = models.FloatField(blank=True, null=True)

  status = models.CharField(max_length=128, blank=False)
  created_time = models.DateTimeField(auto_now_add=True)
  updated_time = models.DateTimeField(auto_now=True)

  def __str__(self):
    return "{}_{}_{}".format(self.name, self.parameters_description, self.goal)

  @classmethod
  def create(cls,
             name,
             parameters_description,
             goal,
             computation_budge,
             theoretical_best_metrics=None):
    instance = cls()
    instance.name = name
    instance.parameters_description = parameters_description
    instance.goal = goal
    instance.computation_budge = computation_budge
    instance.status = "Launch"
    instance.theoretical_best_metrics = theoretical_best_metrics
    instance.save()
    return instance

  @classmethod
  def create_from_dict(self, dict):
    competition = Competition.create(dict["name"],
                                     dict["parameters_description"],
                                     dict["goal"], dict["computation_budge"])

    if "theoretical_best_metrics" in dict:
      competition.theoretical_best_metrics = dict["theoretical_best_metrics"]

    competition.save()

    return competition

  def to_json(self):
    return {
        "id": self.id,
        "name": self.name,
        "parameters_description": self.parameters_description,
        "goal": self.goal,
        "computation_budge": self.computation_budge,
        "theoretical_best_metrics": self.theoretical_best_metrics,
        "current_best_metrics": self.current_best_metrics,
        "status": self.status,
        "created_time": self.created_time,
        "updated_time": self.updated_time
    }


class Participation(models.Model):
  competition = models.ForeignKey(Competition, related_name="competition")
  username = models.CharField(max_length=128, blank=False)
  email = models.CharField(max_length=128, blank=False)

  current_best_metrics = models.FloatField(blank=True, null=True)
  current_trial_count = models.IntegerField(blank=False, default=0)

  status = models.CharField(max_length=128, blank=False)
  created_time = models.DateTimeField(auto_now_add=True)
  updated_time = models.DateTimeField(auto_now=True)

  def __str__(self):
    return "{}_{}_{}".format(self.competition, self.username, self.email)

  @classmethod
  def create(cls, competition, username, email):
    instance = cls()
    instance.competition = competition
    instance.username = username
    instance.email = email
    instance.status = "Active"
    instance.save()
    return instance

  @classmethod
  def create_from_dict(self, dict):
    return Participation.create(dict["competition"], dict["username"],
                                dict["email"])

  def to_json(self):
    return {
        "id": self.id,
        "competition": self.competition.to_json(),
        "username": self.username,
        "email": self.email,
        "current_best_metrics": self.current_best_metrics,
        "current_trial_count": self.current_trial_count,
        "status": self.status,
        "created_time": self.created_time,
        "updated_time": self.updated_time
    }


class Trial(models.Model):
  participation = models.ForeignKey(
      Participation, related_name="participation")
  parameters_instance = models.CharField(max_length=1024, blank=False)
  metrics = models.FloatField(blank=True, null=True)

  status = models.CharField(max_length=128, blank=False)
  created_time = models.DateTimeField(auto_now_add=True)
  updated_time = models.DateTimeField(auto_now=True)

  def __str__(self):
    return "{}".format(self.parameters_instance)

  @classmethod
  def create(cls, participation, parameters_instance):
    instance = cls()
    instance.participation = participation
    instance.parameters_instance = parameters_instance
    instance.status = "NotExecuted"
    instance.save()
    return instance

  @classmethod
  def create_from_dict(self, dict):
    return Trial.create(dict["participation"], dict["parameters_instance"])

  def to_json(self):
    return {
        "id": self.id,
        "participation": self.participation.to_json(),
        "parameters_instance": self.parameters_instance,
        "metrics": self.metrics,
        "status": self.status,
        "created_time": self.created_time,
        "updated_time": self.updated_time
    }
