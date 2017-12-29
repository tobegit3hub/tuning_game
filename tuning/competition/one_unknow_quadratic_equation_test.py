import json

from django.test import TestCase

from one_unknow_quadratic_equation import OneUnknowQuadraticEquation


class OneUnknowQuadraticEquationTest(TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_execute(self):
    # 2 * (1 - 1)**2 -1
    parameters = {"x": 1.0}
    parameters_instance = json.dumps(parameters)
    expected_metrics = -1

    competition = OneUnknowQuadraticEquation()
    metrics = competition.execute(parameters_instance)
    self.assertEqual(metrics, expected_metrics)

    # 2 * (0 - 1)**2 -1
    parameters = {"x": 0.0}
    parameters_instance = json.dumps(parameters)
    expected_metrics = 1

    competition = OneUnknowQuadraticEquation()
    metrics = competition.execute(parameters_instance)
    self.assertEqual(metrics, expected_metrics)
