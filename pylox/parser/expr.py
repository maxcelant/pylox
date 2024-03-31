from __future__ import annotations
from abc import ABC, abstractmethod

from pylox.scanner.token_item import TokenItem


class Expr(ABC):

  @abstractmethod
  def accept(self, visitor: Expr.Visitor):
    pass

  class Visitor(ABC):
    @abstractmethod
    def visit_binary(self, binary: Expr.Binary):
      pass

    @abstractmethod
    def visit_grouping(self, grouping: Expr.Grouping):
      pass

    @abstractmethod
    def visit_literal(self, literal: Expr.Literal):
      pass

    @abstractmethod
    def visit_unary(self, unary: Expr.Unary):
      pass


  class Binary:
    def __init__(self, left: Expr, operator: TokenItem, right: Expr):
      self.left = left
      self.operator = operator
      self.right = right

    def accept(self, visitor: Expr.Visitor):
      return visitor.visit_binary(self)


  class Grouping:
    def __init__(self, expression: Expr):
      self.expression = expression

    def accept(self, visitor: Expr.Visitor):
      return visitor.visit_grouping(self)


  class Literal:
    def __init__(self, value: object):
      self.value = value

    def accept(self, visitor: Expr.Visitor):
      return visitor.visit_literal(self)


  class Unary:
    def __init__(self, operator: TokenItem, right: Expr):
      self.operator = operator
      self.right = right

    def accept(self, visitor: Expr.Visitor):
      return visitor.visit_unary(self)

  
  class Variable:
    def __init__(self, name: TokenItem):
      self.name = name