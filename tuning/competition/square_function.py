import json

from abstract_competition import AbstractCompetition


class SquareFunction(AbstractCompetition):
  """
  The game for testing. Y = x ** 2.
  """

  def execute(self, parameters_instance):

    # Example: {"parameter": 100.0}
    parameters_json = json.loads(parameters_instance)
    parameter = parameters_json["parameter"]

    metrics = parameter**2

    return metrics
