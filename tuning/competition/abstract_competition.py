from abc import ABCMeta, abstractmethod, abstractproperty


class AbstractCompetition(object):
  """
  The abstract class for competitions. All competition should implement the method execute().
  """

  __metaclass__ = ABCMeta

  @abstractmethod
  def execute(self, parameters_instance):
    """
    Args:
      parameters_instance: The parameter json string, example is '{"parameter": 100.0}'. 
    Return:
      The metrics.
    """
    pass
