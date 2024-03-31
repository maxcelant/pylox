

from pylox.interpreter.runtime_exception import RuntimeException
from pylox.scanner.token_item import TokenItem


class Environment:
  def __init__(self):
    self.values = {}

  def define(self, name: str, value: object) -> None:
    self.values[name] = value

  def get(self, name: TokenItem):
    if name.lexeme in self.values:
      return self.values[name.lexeme]
    
    raise RuntimeException(name, f"Undefined variable '{name.lexeme}'.")