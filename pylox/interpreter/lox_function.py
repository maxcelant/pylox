
from pylox.parser.stmt import Stmt
from pylox.interpreter.lox_callable import LoxCallable
from pylox.interpreter.environment import Environment
from pylox.interpreter.interpreter import Interpreter


class LoxFunction(LoxCallable):
  def __init__(self, declaration: Stmt.Function):
    self.declaration = declaration   

  def call(self, interpreter: Interpreter, arguments: list[object]) -> object:
    environment = Environment(interpreter.Globals)
    for i in range(len(self.declaration.params)):
      environment.define(self.declaration.params[i].lexeme, arguments[i])
    interpreter.execute_block(self.declaration.body, environment)
