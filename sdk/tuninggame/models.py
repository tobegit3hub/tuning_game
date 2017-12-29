class Competition(object):
  def __init__(self,
               name,
               parameters_description,
               goal,
               computation_budge,
               id=None,
               theoretical_best_metrics=None,
               current_best_metrics=None,
               status=None,
               created_time=None,
               updated_time=None):
    self.id = id
    self.name = name
    self.parameters_description = parameters_description
    self.goal = goal
    self.computation_budge = computation_budge
    self.theoretical_best_metrics = theoretical_best_metrics
    self.current_best_metrics = current_best_metrics
    self.status = status
    self.created_time = created_time
    self.updated_time = updated_time

  def __str__(self):
    return "{}_{}_{}".format(self.name, self.parameters_description, self.goal)

  def to_dict(self):
    return {
        "name": self.name,
        "parameters_description": self.parameters_description,
        "goal": self.goal,
        "computation_budge": self.computation_budge
    }

  @classmethod
  def create_from_dict(self, dict):
    return Competition(dict["name"], dict["parameters_description"],
                       dict["goal"], dict["computation_budge"], dict["id"],
                       dict["theoretical_best_metrics"],
                       dict["current_best_metrics"], dict["status"],
                       dict["created_time"], dict["updated_time"])


class Participation(object):
  def __init__(self,
               competition_id,
               username,
               email,
               id=None,
               current_best_metrics=None,
               current_trial_count=None,
               status=None,
               created_time=None,
               updated_time=None):
    self.id = id
    self.competition_id = competition_id
    self.username = username
    self.email = email
    self.current_best_metrics = current_best_metrics
    self.current_trial_count = current_trial_count
    self.status = status
    self.created_time = created_time
    self.updated_time = updated_time

  def __str__(self):
    return "{}_{}_{}".format(self.competition, self.username, self.email)

  def to_dict(self):
    return {
        "competition_id": self.competition_id,
        "username": self.username,
        "email": self.email
    }

  @classmethod
  def create_from_dict(self, dict):
    return Participation(
        dict["competition"]["id"], dict["username"], dict["email"], dict["id"],
        dict["current_best_metrics"], dict["current_trial_count"],
        dict["status"], dict["created_time"], dict["updated_time"])


class Trial(object):
  def __init__(self,
               participation_id,
               parameters_instance,
               id=None,
               metrics=None,
               status=None,
               created_time=None,
               updated_time=None):
    self.id = id
    self.participation_id = participation_id
    self.parameters_instance = parameters_instance
    self.metrics = metrics
    self.status = status
    self.created_time = created_time
    self.updated_time = updated_time

  def __str__(self):
    return "{}".format(self.parameters_instance)

  def to_dict(self):
    return {
        "participation_id": self.participation_id,
        "parameters_instance": self.parameters_instance
    }

  @classmethod
  def create_from_dict(self, dict):
    return Trial(dict["participation"]["id"], dict["parameters_instance"],
                 dict["id"], dict["metrics"], dict["status"],
                 dict["created_time"], dict["updated_time"])
