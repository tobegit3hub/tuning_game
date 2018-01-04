from django.core.management.base import BaseCommand

from tuning.models import Competition, Participation, Trial


class Command(BaseCommand):
  args = ""
  help = "Initialize the database with competitions data"

  def _create_competitions_participations_trials(self):

    # Check if we need to initialize database or not
    competition_count = Competition.objects.count()
    if competition_count > 0:
      print("There are {} competitions in databases, exit now".format(
          competition_count))
      return

    # ReturnInputGame
    competition_dict = {
        "name":
        "ReturnInputGame",
        "introduction":
        "The game will return the exact number of the input. It has only one parameter.",
        "parameters_description":
        '{"params":[{"parameterName": "parameter", "type": "DOUBLE"}]}',
        "goal":
        "MAXIMIZE",
        "computation_budge":
        100,
        "theoretical_best_metrics":
        9223372036854775807
    }
    competition = Competition.create_from_dict(competition_dict)

    participation_dict = {
        "competition": competition,
        "username": "test",
        "email": "test@gmail.com"
    }
    participation = Participation.create_from_dict(participation_dict)

    trial_dict = {
        "participation": participation,
        "parameters_instance": '{"parameter": 10.0}'
    }
    Trial.create_from_dict(trial_dict)

    # SquareFunction
    competition_dict = {
        "name":
        "SquareFunction",
        "introduction":
        "The game will return the square of the input. It has only one parameter.",
        "parameters_description":
        '{"params":[{"parameterName": "parameter", "type": "DOUBLE"}]}',
        "goal":
        "MAXIMIZE",
        "computation_budge":
        100,
        "theoretical_best_metrics":
        9223372036854775807
    }
    competition = Competition.create_from_dict(competition_dict)

    participation_dict = {
        "competition": competition,
        "username": "test",
        "email": "test@gmail.com"
    }
    participation = Participation.create_from_dict(participation_dict)

    trial_dict = {
        "participation": participation,
        "parameters_instance": '{"parameter": 10.0}'
    }
    Trial.create_from_dict(trial_dict)

    # OneUnknowQuadraticEquation
    competition_dict = {
        "name":
        "OneUnknowQuadraticEquation",
        "introduction":
        "The uderlying game is the quadratic equation with one unknow variable which has the optimal value. It has only one parameter.",
        "parameters_description":
        '{"params":[{"parameterName": "x", "type": "DOUBLE"}]}',
        "goal":
        "MINIMIZE",
        "computation_budge":
        100,
        "theoretical_best_metrics":
        -1.0,
    }
    competition = Competition.create_from_dict(competition_dict)

    participation_dict = {
        "competition": competition,
        "username": "test",
        "email": "test@gmail.com"
    }
    participation = Participation.create_from_dict(participation_dict)

    trial_dict = {
        "participation": participation,
        "parameters_instance": '{"x": 10.0}'
    }
    Trial.create_from_dict(trial_dict)

    # MnistKerasDnn
    competition_dict = {
        "name":
        "MnistKerasDnn",
        "introduction":
        "The uderlying game is the Keras DNN model for MNIST dataset. It has only three parameter.",
        "parameters_description":
        '{"params":[{"parameterName": "batch_size", "type": "INTEGER"}, {"parameterName": "hidden1_number", "type": "INTEGER"}, {"parameterName": "hidden2_number", "type": "INTEGER"}]}',
        "goal":
        "MAXIMIZE",
        "computation_budge":
        100,
        "theoretical_best_metrics":
        1.0,
    }
    competition = Competition.create_from_dict(competition_dict)

    participation_dict = {
        "competition": competition,
        "username": "test",
        "email": "test@gmail.com"
    }
    participation = Participation.create_from_dict(participation_dict)

    trial_dict = {
        "participation":
        participation,
        "parameters_instance":
        'parameters = {"batch_size": 128, "hidden1_number": 512, "hidden2_number": 512}'
    }
    Trial.create_from_dict(trial_dict)

    # TwoUnknowQuadraticEquation
    competition_dict = {
        "name":
            "TwoUnknowQuadraticEquation",
        "introduction":
            "The uderlying game is the quadratic equation with two unknow variables which has the optimal value. It has two parameters.",
        "parameters_description":
            '{"params":[{"parameterName": "x1", "type": "DOUBLE"}, {"parameterName": "x2", "type": "DOUBLE"}]}',
        "goal":
            "MAXIMIZE",
        "computation_budge":
            100,
        "theoretical_best_metrics":
            100.0,
    }
    competition = Competition.create_from_dict(competition_dict)

    participation_dict = {
        "competition": competition,
        "username": "test",
        "email": "test@gmail.com"
    }
    participation = Participation.create_from_dict(participation_dict)

    trial_dict = {
        "participation": participation,
        "parameters_instance": '{"x1": 1.0, "x2": 2.0}'
    }
    Trial.create_from_dict(trial_dict)

    competition_count = Competition.objects.count()
    participation_count = Participation.objects.count()
    trial_count = Trial.objects.count()

    print("Add {} competitions, {} participations, {} trials in database".
          format(competition_count, participation_count, trial_count))

  def handle(self, *args, **options):
    self._create_competitions_participations_trials()
