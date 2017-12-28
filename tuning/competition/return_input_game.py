import json

from abstract_competition import AbstractCompetition


class ReturnInputGame(AbstractCompetition):
  """
  The game for testing. Y = x.
  """

  def execute(self, parameters_instance):

    # Example: {"parameter": 100.0}
    parameters_json = json.loads(parameters_instance)
    parameter = parameters_json["parameter"]

    metrics = parameter

    return metrics
