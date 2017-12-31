#!/usr/bin/env python

from tuninggame.client import TuningGameClient

endpoint = "http://127.0.0.1:8000"
competition_name = "SquareFunction"
username = "tobe"
client = TuningGameClient(endpoint)


def registry_participation():
  email = "tobeg3oogle@gmail.com"
  competition = client.get_competition_by_name(competition_name)
  client.create_participation(competition.id, username, email)


def run_trials():
  participation = client.get_participation_by_competition_name_and_username(
      competition_name, username)

  parameters_instance = {"parameter": 10}
  trial = client.create_trial(participation.id, parameters_instance)
  client.execute_trial(trial.id)

  parameters_instance = {"parameter": -5}
  trial = client.create_trial(participation.id, parameters_instance)
  client.execute_trial(trial.id)

  parameters_instance = {"parameter": 1}
  trial = client.create_trial(participation.id, parameters_instance)
  client.execute_trial(trial.id)


def check_result():
  participation = client.get_participation_by_competition_name_and_username(
      competition_name, username)
  client.print_participation_result(participation.id)


def main():
  print("Play SquareFunction competition")

  # Register for the first time
  #registry_participation()

  # Run more times with other parameters
  #run_trials()

  # Check the current result
  check_result()


if __name__ == "__main__":
  main()
