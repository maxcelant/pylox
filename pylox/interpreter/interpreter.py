
from typing import Callable
from pylox.interpreter.environment import Environment
from pylox.parser.expr import Expr
from pylox.parser.stmt import Stmt
from pylox.scanner.token_type import TokenType
from pylox.interpreter.runtime_exception import RuntimeException


class Interpreter(Expr.Visitor, Stmt.Visitor):

  def __init__(self, error_callback: Callable[[RuntimeException], None]):
    self.error_callback = error_callback
    self.environment = Environment()


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


  def is_truthy(self, obj: object) -> bool:
    if obj == None: return False
    if isinstance(obj, bool): return bool(obj)
    return True


  def is_equal(self, a: object, b: object) -> bool:
    if a == None and b == None: return True
    if a == None: return False
    return a == b


  def check_number_operand(self, operator: TokenType, operand: object):
    if isinstance(operand, float): return
    raise RuntimeException(operator, "Operand must be a number.")


  def check_number_operands(self, operator: TokenType, left: object, right: object):
    if isinstance(left, float) and isinstance(right, float): 
      return
    raise RuntimeException(operator, "Operand must be a number.")


  def visit_expression_stmt(self, stmt: Stmt.Expression) -> None:
    self.evaluate(stmt.expression)


  def visit_print_stmt(self, stmt: Stmt.Print) -> None:
    value: object = self.evaluate(stmt.expression)
    print(self.stringify(value))


  def visit_var_stmt(self, stmt: Stmt.Var) -> None:
    value: object = None
    if stmt.initializer:
      value = self.evaluate(stmt.initializer)
    self.environment.define(stmt.name.lexeme, value)


  def visit_literal_expr(self, expr: Expr.Literal):
    return expr.value


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
  

  def visit_assign_expr(self, assign: Expr.Assign):
    pass # todo
  

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
    