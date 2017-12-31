import json

from django.test import TestCase

from mnist_keras_dnn import MnistKerasDnn


class MnistKerasDnnTest(TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_execute(self):

    parameters = {"batch_size": 128, "hidden1_number": 512, "hidden2_number": 512}
    parameters_instance = json.dumps(parameters)
    expected_max_metrics = 0.98
    expected_min_metrics = 0.95

    competition = MnistKerasDnn()
    metrics = competition.execute(parameters_instance)

    # Around 0.9683
    self.assertTrue(metrics < expected_max_metrics)
    self.assertTrue(metrics > expected_min_metrics)
