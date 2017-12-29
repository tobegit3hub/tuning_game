#!/usr/bin/env python

from tuninggame.client import TuningGameClient

def main():

  endpoint = "http://127.0.0.1:8000"
  client = TuningGameClient(endpoint)

  competitions = client.list_competitions()
  print(competitions)

  participations = client.list_participations()
  print(participations)

  trials = client.list_trials()
  print(trials)


if __name__ == "__main__":
  main()
