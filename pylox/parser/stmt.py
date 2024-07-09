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
    def visit_while_stmt(self, stmt: Stmt.While):
      pass

    @abstractmethod
    def visit_if_stmt(self, stmt: Stmt.If):
      pass

    @abstractmethod
    def visit_function_stmt(self, stmt: Stmt.Function):
      pass

    @abstractmethod
    def visit_block_stmt(self, stmt: Stmt.Block):
      pass

    @abstractmethod
    def visit_expression_stmt(self, stmt: Stmt.Expression):
      pass

    @abstractmethod
    def visit_print_stmt(self, stmt: Stmt.Print):
      pass

    @abstractmethod
    def visit_var_stmt(self, stmt: Stmt.Var):
      pass


  class While:
    def __init__(self, condition: Expr, body: Stmt):
      self.condition = condition
      self.body      = body

    def accept(self, visitor: Stmt.Visitor):
      visitor.visit_while_stmt(self)

    def __repr__(self):
      return f'Stmt.Function(\n  {self.condition=}\n  {self.body}\n)'

  class If:
    def __init__(self, condition: Expr, then_branch: Stmt, else_branch: Stmt | None):
      self.condition   = condition
      self.then_branch = then_branch
      self.else_branch = else_branch

    def accept(self, visitor: Stmt.Visitor):
      visitor.visit_if_stmt(self)

    def __repr__(self):
      return f'Stmt.If(\n  {self.condition=}\n  {self.then_branch=}\n  {self.else_branch=}\n)'

  class Function:
    def __init__(self, name: TokenItem, params: list[TokenItem], body: list[Stmt]):
      self.name   = name
      self.params = params
      self.body   = body

    def accept(self, visitor: Stmt.Visitor):
        visitor.visit_function_stmt(self)

    def __repr__(self):
        return f'Stmt.Function(\n  {self.name=}\n  {self.params=}\n  {self.body})'


  class Block:
    def __init__(self, statements: list[Stmt]):
      self.statements = statements

    def accept(self, visitor: Stmt.Visitor):
      visitor.visit_block_stmt(self)

    def __repr__(self):
      return "Stmt.Block(" + ',\n'.join([repr(s) for s in self.statements])


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
    
