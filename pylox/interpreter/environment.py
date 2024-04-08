from __future__ import annotations
from pylox.interpreter.runtime_exception import RuntimeException
from pylox.scanner.token_item import TokenItem


class Environment:
  def __init__(self, enclosing: Environment | None = None):
    self.values = {}
    self.enclosing = enclosing

  def define(self, name: str, value: object) -> None:
    self.values[name] = value

  def get(self, name: TokenItem):
    if name.lexeme in self.values:
      return self.values[name.lexeme]
    if self.enclosing:
      return self.enclosing.get(name)
    
    raise RuntimeException(name, f"Undefined variable '{name.lexeme}'.")
  
  def assign(self, name: TokenItem, value: object) -> None:
    if name.lexeme in self.values:
      self.values[name.lexeme] = value
      return
    
    if self.enclosing:
      self.enclosing.assign(name, value)
      return
    
    raise RuntimeException(name, f"Undefined variable '{name.lexeme}'.")