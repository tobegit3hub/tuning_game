# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Competition(models.Model):
  name = models.CharField(max_length=128, blank=False)
  parameters_description = models.CharField(max_length=1024, blank=False)
  computation_budge = models.IntegerField(blank=False)
  theoretical_best_metrics = models.FloatField(blank=True, null=True)

  current_best_metrics = models.FloatField(blank=True, null=True)

  status = models.CharField(max_length=128, blank=False)
  created_time = models.DateTimeField(auto_now_add=True)
  updated_time = models.DateTimeField(auto_now=True)

  def __str__(self):
    return "{}".format(self.name)

  @classmethod
  def create(cls, name, parameters_description, status):
    instance = cls()
    instance.name = name
    instance.parameters_description = parameters_description
    instance.status = status
    return instance

  def to_json(self):
    return {"id": self.id, "name": self.name}


class Participation(models.Model):
  competition = models.ForeignKey(Competition, related_name="competition")
  username = models.CharField(max_length=128, blank=False)
  email = models.CharField(max_length=128, blank=False)

  current_best_metrics = models.FloatField(blank=True, null=True)
  current_tiral_count = models.IntegerField(blank=True, null=True)

  status = models.CharField(max_length=128, blank=False)
  created_time = models.DateTimeField(auto_now_add=True)
  updated_time = models.DateTimeField(auto_now=True)

  def __str__(self):
    return "{}_{}".format(self.competition, self.username)

  def to_json(self):
    return {"id": self.id, "username": self.username, "email": self.email}


class Trial(models.Model):
  particiption = models.ForeignKey(Participation, related_name="participation")
  parameters_instance = models.CharField(max_length=1024, blank=False)
  metrics = models.FloatField(blank=True, null=True)

  status = models.CharField(max_length=128, blank=False)
  created_time = models.DateTimeField(auto_now_add=True)
  updated_time = models.DateTimeField(auto_now=True)

  def __str__(self):
    return "{}_{}".format(self.particiption, self.parameters_instance)

  def to_json(self):
    return {
        "id": self.id,
        "parameters_instance": self.parameters_instance,
        "metrics": self.metrics
    }
