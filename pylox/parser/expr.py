from __future__ import annotations
from abc import ABC, abstractmethod

from pylox.scanner.token_item import TokenItem


class Expr(ABC):

  @abstractmethod
  def accept(self, visitor: Expr.Visitor):
    pass

  class Visitor(ABC):

    @abstractmethod
    def visit_assign_expr(self, expr: Expr.Assign):
      pass
    
    @abstractmethod
    def visit_binary_expr(self, expr: Expr.Binary):
      pass

    @abstractmethod
    def visit_call_expr(self, expr: Expr.Call):
      pass

    @abstractmethod
    def visit_grouping_expr(self, expr: Expr.Grouping):
      pass

    @abstractmethod
    def visit_literal_expr(self, expr: Expr.Literal):
      pass

    @abstractmethod
    def visit_logical_expr(self, expr: Expr.Logical):
      pass

    @abstractmethod
    def visit_variable_expr(self, expr: Expr.Variable):
      pass

    @abstractmethod
    def visit_unary_expr(self, expr: Expr.Unary):
      pass


  class Assign:
    def __init__(self, name: TokenItem, value: Expr):
      self.name = name
      self.value = value

    def accept(self, visitor: Expr.Visitor):
      return visitor.visit_assign_expr(self)
    
    def __repr__(self):
      return f'Assign({self.name=}, {self.value=})'


  class Binary:
    def __init__(self, left: Expr, operator: TokenItem, right: Expr):
      self.left = left
      self.operator = operator
      self.right = right

    def accept(self, visitor: Expr.Visitor):
      return visitor.visit_binary_expr(self)
    
    def __repr__(self):
      return f'Binary({self.left=}, {self.operator=}, {self.right})'
    
  
  class Call:
    def __init__(self, callee: Expr, paren: TokenItem, arguments: list[Expr]):
      self.callee = callee
      self.paren = paren
      self.arguments = arguments

    def accept(self, visitor: Expr.Visitor):
      return visitor.visit_call_expr(self)


  class Grouping:
    def __init__(self, expression: Expr):
      self.expression = expression

    def accept(self, visitor: Expr.Visitor):
      return visitor.visit_grouping_expr(self)

    def __repr__(self):
      return f'Grouping({self.expression=})'


  class Literal:
    def __init__(self, value: object):
      self.value = value

    def accept(self, visitor: Expr.Visitor):
      return visitor.visit_literal_expr(self)

    def __repr__(self):
      return f'Literal({self.value=})'
    
  
  class Logical:
    def __init__(self, left: Expr, operator: TokenItem, right: Expr):
      self.left = left
      self.operator = operator
      self.right = right

    def accept(self, visitor: Expr.Visitor):
      return visitor.visit_logical_expr(self)

    def __repr__(self):
      return f'Logical({self.left=}, {self.operator=}, {self.right=})'

  
  class Variable:
    def __init__(self, name: TokenItem):
      self.name = name

    def accept(self, visitor: Expr.Visitor):
      return visitor.visit_variable_expr(self)

    def __repr__(self):
      return f'Variable({self.name=})'
    
    
  class Unary:
    def __init__(self, operator: TokenItem, right: Expr):
      self.operator = operator
      self.right = right

    def accept(self, visitor: Expr.Visitor):
      return visitor.visit_unary_expr(self)

    def __repr__(self):
      return f'Unary({self.operator=}, {self.right=})'