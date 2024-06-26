
from typing import Callable
from pylox.interpreter.environment import Environment
from pylox.parser.expr import Expr
from pylox.parser.stmt import Stmt
from pylox.scanner.token_type import TokenType
from pylox.scanner.token_item import TokenItem
from pylox.interpreter.runtime_exception import RuntimeException


class Interpreter(Expr.Visitor, Stmt.Visitor):

  def __init__(self, error_callback: Callable[[RuntimeException], None]):
    from pylox.interpreter.clock_function import ClockFunction
    self.error_callback = error_callback
    self.Globals = Environment()
    self.environment = self.Globals
    self.Globals.define("clock", ClockFunction())


  def interpret(self, statements: list[Stmt]):
    try:
      for s in statements:
        self.execute(s)
    except RuntimeException as e:
      self.error_callback(e)

  
  def stringify(self, obj: object):
    if obj == None: return "nil"

    if isinstance(obj, float):
      text = str(obj)
      if text.endswith('.0'):
        text = text[0:len(text) - 2]
      return text
    
    return str(obj)


  def evaluate(self, expr: Expr):
    return expr.accept(self)


  def execute(self, stmt: Stmt):
    stmt.accept(self)

  
  def execute_block(self, statements: list[Stmt], environment: Environment):
    previous = self.environment
    try:
      self.environment = environment
      for stmt in statements:
        self.execute(stmt)
    finally:
      self.environment = previous


  def is_truthy(self, obj: object) -> bool:
    if obj == None: return False
    if isinstance(obj, bool): return bool(obj)
    return True


  def is_equal(self, a: object, b: object) -> bool:
    if a == None and b == None: return True
    if a == None: return False
    return a == b


  def check_number_operand(self, operator: TokenItem, operand: object):
    if isinstance(operand, float): return
    raise RuntimeException(operator, "Operand must be a number.")


  def check_number_operands(self, operator: TokenItem, left: object, right: object):
    if isinstance(left, float) and isinstance(right, float): 
      return
    raise RuntimeException(operator, "Operand must be a number.")


  def visit_expression_stmt(self, stmt: Stmt.Expression) -> None:
    self.evaluate(stmt.expression)


  def visit_function_stmt(self, stmt: Stmt.Function) -> None:
    from pylox.interpreter.lox_function import LoxFunction
    function: LoxFunction = LoxFunction(stmt)
    self.environment.define(stmt.name.lexeme, function)


  def visit_if_stmt(self, stmt: Stmt.If) -> None:
    if self.is_truthy(self.evaluate(stmt.condition)):
      self.execute(stmt.then_branch)
    elif stmt.else_branch:
      self.execute(stmt.else_branch)


  def visit_print_stmt(self, stmt: Stmt.Print) -> None:
    value: object = self.evaluate(stmt.expression)
    print(self.stringify(value))


  def visit_var_stmt(self, stmt: Stmt.Var) -> None:
    value: object = None
    if stmt.initializer:
      value = self.evaluate(stmt.initializer)
    self.environment.define(stmt.name.lexeme, value)

  
  def visit_while_stmt(self, stmt: Stmt.While) -> None:
    while self.is_truthy(self.evaluate(stmt.condition)):
      self.execute(stmt.body)


  def visit_block_stmt(self, stmt: Stmt.Block):
    self.execute_block(stmt.statements, Environment(enclosing=self.environment))


  def visit_literal_expr(self, expr: Expr.Literal):
    return expr.value
  

  def visit_logical_expr(self, expr: Expr.Logical):
    left: object = self.evaluate(expr.left)

    if expr.operator.token_type == TokenType.OR:
      if self.is_truthy(left): 
        return left
    else:
      if not self.is_truthy(left): 
        return left
      
    return self.evaluate(expr.right)


  def visit_grouping_expr(self, expr: Expr.Grouping):
    return self.evaluate(expr.expression)


  def visit_unary_expr(self, expr: Expr.Unary):
    right: object = self.evaluate(expr.right)

    if expr.operator.token_type == TokenType.MINUS:
      self.check_number_operand(expr.operator, right)
      return -float(right)
    
    if expr.operator.token_type == TokenType.BANG:
      return not self.is_truthy(right)
    
  
  def visit_variable_expr(self, expr: Expr.Variable):
    return self.environment.get(expr.name)
  

  def visit_assign_expr(self, expr: Expr.Assign):
    value: object = self.evaluate(expr.value)
    self.environment.assign(expr.name, value)
    return value
  

  def visit_binary_expr(self, expr: Expr.Binary):
    right: object = self.evaluate(expr.right)
    left: object = self.evaluate(expr.left)

    if expr.operator.token_type == TokenType.BANG_EQUAL:
      return not self.is_equal(left, right)
   
    if expr.operator.token_type == TokenType.EQUAL_EQUAL:
      return self.is_equal(left, right)

    if expr.operator.token_type == TokenType.GREATER:
      self.check_number_operands(expr.operator, left, right)
      return float(left) > float(right)
    
    if expr.operator.token_type == TokenType.GREATER_EQUAL:
      self.check_number_operands(expr.operator, left, right)
      return float(left) >= float(right)
    
    if expr.operator.token_type == TokenType.LESS:
      self.check_number_operands(expr.operator, left, right)
      return float(left) < float(right)
    
    if expr.operator.token_type == TokenType.LESS_EQUAL:
      self.check_number_operands(expr.operator, left, right)
      return float(left) <= float(right)

    if expr.operator.token_type == TokenType.MINUS:
      self.check_number_operands(expr.operator, left, right)
      return float(left) - float(right)
    
    if expr.operator.token_type == TokenType.PLUS:
      if isinstance(left, float) and isinstance(right, float):
        return float(left) + float(right)
      if isinstance(left, str) and isinstance(right, str):
        return str(left) + str(right)
      raise RuntimeException(expr.operator, "Operand must be two numbers or two strings.")
      
    if expr.operator.token_type == TokenType.SLASH:
      self.check_number_operands(expr.operator, left, right)
      return float(left) / float(right)
    
    if expr.operator.token_type == TokenType.STAR:
      self.check_number_operands(expr.operator, left, right)
      return float(left) * float(right)
    

  def visit_call_expr(self, expr: Expr.Call):
    from pylox.interpreter.lox_callable import LoxCallable
    function = self.evaluate(expr.callee)

    arguments: list[object] = []
    for arg in expr.arguments:
      arguments.append(self.evaluate(arg))

    if not isinstance(function, LoxCallable):
      return self.error_callback('Can only call functions and classes.')
    if len(arguments) != function.arity():
      return self.error_callback(f'Expected {function.arity()} arguments but got {len(arguments)}.')
    
    return function.call(self, arguments)



