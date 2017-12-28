import json

from django.test import TestCase

from return_input_game import ReturnInputGame


class ReturnInputGameTest(TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_execute(self):
    parameters = {"parameter": 100.0}
    parameters_instance = json.dumps(parameters)
    expected_metrics = 100.0

    competition = ReturnInputGame()
    metrics = competition.execute(parameters_instance)

    self.assertEqual(metrics, expected_metrics)
