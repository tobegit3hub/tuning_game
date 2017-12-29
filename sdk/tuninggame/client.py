import json
import logging

import requests

from .models import Competition, Participation, Trial


class TuningGameClient(object):
  def __init__(self, endpoint="http://0.0.0.0:8000"):
    self.endpoint = endpoint

  def create_competition(self, name, parameters_description, goal,
                         computation_budge):
    url = "{}/tuning/v1/competitions".format(self.endpoint)
    request_data = {
        "name": name,
        "parameters_description": parameters_description,
        "goal": goal,
        "computation_budge": computation_budge
    }
    response = requests.post(url, json=request_data)

    competition = None
    if response.ok:
      competition = Competition.from_dict(response.json()["data"])

    return competition

  def list_competitions(self):
    url = "{}/tuning/v1/competitions".format(self.endpoint)
    response = requests.get(url)

    competitions = []
    if response.ok:
      dicts = response.json()["data"]
      for dict in dicts:
        competition = Competition.create_from_dict(dict)
        competitions.append(competition)

    return competitions

  def get_competition_by_id(self, competition_id):
    url = "{}/tuning/v1/competitions/{}".format(self.endpoint, competition_id)
    response = requests.get(url)

    competition = None
    if response.ok:
      competition = Competition.create_from_dict(response.json()["data"])

    return competition

  def delete_competition(self, competition_id):
    url = "{}/tuning/v1/competitions/{}".format(self.endpoint, competition_id)
    response = requests.delete(url)
    return response

  def create_participation(self, competition_id, username, email):
    url = "{}/tuning/v1/participations".format(self.endpoint)
    request_data = {
        "competition_id": competition_id,
        "username": username,
        "email": email
    }
    response = requests.post(url, json=request_data)

    participation = None
    if response.ok:
      participation = Participation.from_dict(response.json()["data"])

    return participation

  def list_participations(self):
    url = "{}/tuning/v1/participations".format(self.endpoint)
    response = requests.get(url)

    participations = []
    if response.ok:
      dicts = response.json()["data"]
      for dict in dicts:
        participation = Participation.create_from_dict(dict)
        participations.append(participation)

    return participations

  def get_participation_by_id(self, participation_id):
    url = "{}/tuning/v1/participations/{}".format(self.endpoint,
                                                  participation_id)
    response = requests.get(url)

    participation = None
    if response.ok:
      participation = Participation.create_from_dict(response.json()["data"])
    return participation

  def create_trial(self, particiption_id, parameters_instance):
    url = "{}/tuning/v1/trials".format(self.endpoint)
    request_data = {
        "particiption_id": particiption_id,
        "parameters_instance": parameters_instance
    }
    response = requests.post(url, json=request_data)

    trial = None
    if response.ok:
      trial = Trial.create_from_dict(response.json()["data"])

    return trial

  def list_trials(self):
    url = "{}/tuning/v1/trials".format(self.endpoint)
    response = requests.get(url)

    trials = []
    if response.ok:
      dicts = response.json()["data"]
      for dict in dicts:
        trial = Trial.create_from_dict(dict)
        trials.append(trial)

    return trials

  def get_trial_by_id(self, trial_id):
    url = "{}/tuning/v1/trials/{}".format(self.endpoint, trial_id)
    response = requests.get(url)

    trial = None
    if response.ok:
      trial = Trial.create_from_dict(response.json()["data"])

    return trial

  def delete_trial(self, trial_id):
    url = "{}/tuning/v1/trials/{}".format(self.endpoint, trial_id)
    response = requests.delete(url)
    return response

  def execute_trial(self, trial_id):
    url = "{}/tuning/v1/trials/{}/execute".format(self.endpoint, trial_id)
    response = requests.post(url)
    return response
