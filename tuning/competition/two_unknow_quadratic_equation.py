import json

from abstract_competition import AbstractCompetition


class TwoUnknowQuadraticEquation(AbstractCompetition):
  """
    Y = -2 * (x1 + 4)**2 - (x2 - 6)**2 + 100, the best parameters are x1=-2, x2=5 and the best metrics is 100.
    """

  def execute(self, parameters_instance):

    # Example: {"x1": 1.0, "x2": 2.0}
    parameters_json = json.loads(parameters_instance)
    x1 = parameters_json["x1"]
    x2 = parameters_json["x2"]

    metrics = -2 * (x1 + 4)**2 - (x2 - 6)**2 + 100

    return metrics
