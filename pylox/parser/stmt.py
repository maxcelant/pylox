from __future__ import annotations
from abc import ABC, abstractmethod
from pylox.parser.expr import Expr


class Stmt(ABC):

  @abstractmethod
  def accept(self, visitor: Stmt.Visitor):
    pass


  class Visitor(ABC):
    @abstractmethod
    def visit_print_stmt(self, expr: Stmt.Expr):
      pass


    @abstractmethod
    def visit_expression_stmt(self, expr: Stmt.Expr):
      pass


  class Expression:
    def __init__(self, expression: Expr):
      self.expression = expression


    def accept(self, visitor: Stmt.Visitor):
      visitor.visit_expression_stmt(self)


  class Print:
    def __init__(self, expression: Expr):
      self.expression = expression


    def accept(self, visitor: Stmt.Visitor):
      visitor.visit_print_stmt(self)