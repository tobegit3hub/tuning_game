#!/usr/bin/env python

from tuninggame.client import TuningGameClient


def main():

  endpoint = "http://0.0.0.0:8000"
  client = TuningGameClient(endpoint)

  print("Create competition and participation for test")
  competition = client.create_competition("TestCompetition", {}, "MAXIMIZE",
                                          100)
  participation = client.create_participation(competition.id, "TestUser",
                                              "test@gmail.com")

  print("Try to list trials")
  trials = client.list_trials()
  print(trials)

  print("Try to create trial")
  trial = client.create_trial(participation.id, {"parameter": 10.0})
  print(trial)

  print("Try to get trial by id")
  get_trial = client.get_trial_by_id(trial.id)
  print(get_trial)

  print("Try to delete trial")
  client.delete_trial(get_trial.id)

  print("Try to list trials")
  trials = client.list_trials()
  print(trials)

  print("Delete competition and participation for test")
  client.delete_participation(participation.id)
  client.delete_competition(competition.id)


if __name__ == "__main__":
  main()
