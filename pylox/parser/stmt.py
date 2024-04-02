from __future__ import annotations
from abc import ABC, abstractmethod
from pylox.parser.expr import Expr
from pylox.scanner.token_item import TokenItem


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

    @abstractmethod
    def visit_var_stmt(self, expr: Stmt.Expr):
      pass


  class Expression:
    def __init__(self, expression: Expr):
      self.expression = expression

    def accept(self, visitor: Stmt.Visitor):
      visitor.visit_expression_stmt(self)

    def __repr__(self):
      return f'Stmt.Expression({self.expression=})'


  class Print:
    def __init__(self, expression: Expr):
      self.expression = expression

    def accept(self, visitor: Stmt.Visitor):
      visitor.visit_print_stmt(self)

    def __repr__(self):
      return f'Stmt.Print({self.expression=})'


  class Var:
    def __init__(self, name: TokenItem, initializer: Expr):
      self.name = name
      self.initializer = initializer

    def accept(self, visitor: Stmt.Visitor):
      visitor.visit_var_stmt(self)

    def __repr__(self):
      return f'Stmt.Var({self.name=}, {self.initializer=})'
    
