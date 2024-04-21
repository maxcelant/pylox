
from abc import ABC, abstractmethod

from pylox.interpreter.interpreter import Interpreter


class LoxCallable(ABC):
  
  @abstractmethod
  def call(interpreter: Interpreter, arguments: list[object]):
    pass