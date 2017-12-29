import json

from abstract_competition import AbstractCompetition


class OneUnknowQuadraticEquation(AbstractCompetition):
  """
    Y = 2 * (x - 1)**2 - 1, the best x is 1 and the best metrics is -1.
    """

  def execute(self, parameters_instance):

    # Example: {"x": 100.0}
    parameters_json = json.loads(parameters_instance)
    x = parameters_json["x"]

    metrics = 2 * (x - 1)**2 - 1

    return metrics
