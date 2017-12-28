import json

from django.test import TestCase

from square_function import SquareFunction


class SquareFunctionTest(TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_execute(self):
    parameters = {"parameter": 100.0}
    parameters_instance = json.dumps(parameters)
    expected_metrics = 100.0**2

    competition = SquareFunction()
    metrics = competition.execute(parameters_instance)

    self.assertEqual(metrics, expected_metrics)
