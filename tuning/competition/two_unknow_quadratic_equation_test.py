import json

from django.test import TestCase

from two_unknow_quadratic_equation import TwoUnknowQuadraticEquation


class TwoUnknowQuadraticEquationTest(TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_execute(self):
    # -2 * (1.0 + 4)**2 - (2.0 - 6)**2 + 100
    parameters = {"x1": 1.0, "x2": 2.0}
    parameters_instance = json.dumps(parameters)
    expected_metrics = 34.0

    competition = TwoUnknowQuadraticEquation()
    metrics = competition.execute(parameters_instance)
    self.assertEqual(metrics, expected_metrics)

    # -2 * (-1.0 + 4)**2 - (5.0 - 6)**2 + 100
    parameters = {"x1": -1.0, "x2": 5.0}
    parameters_instance = json.dumps(parameters)
    expected_metrics = 81.0

    competition = TwoUnknowQuadraticEquation()
    metrics = competition.execute(parameters_instance)
    self.assertEqual(metrics, expected_metrics)
