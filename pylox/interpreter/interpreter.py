
from pylox.parser.productions import Expr, Visitor
from pylox.scanner.token_type import TokenType
from pylox.interpreter.runtime_exception import RuntimeException


class Interpreter(Visitor):

  def __init__(self, error_callback):
    self.error_callback = error_callback

  def interpret(self, expression: Expr):
    try:
      value: object = self.evaluate(expression)
      print(self.stringify(value))
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

  def visit_literal(self, expr: Expr.Literal):
    return expr.value
  
  def visit_grouping(self, expr: Expr.Grouping):
    return self.evaluate(expr.expression)
  
  def visit_unary(self, expr: Expr.Unary):
    right: object = self.evaluate(expr.right)

    if expr.operator.token_type == TokenType.MINUS:
      self.check_number_operand(expr.operator, right)
      return -float(right)
    
    if expr.operator.token_type == TokenType.BANG:
      return not self.is_truthy(right)
  
  def visit_binary(self, expr: Expr.Binary):
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
    