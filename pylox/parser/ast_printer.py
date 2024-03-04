
from pylox.parser.productions import Expr, Visitor
from pylox.scanner.token_item import TokenItem
from pylox.scanner.token_type import TokenType




class AstPrinter(Visitor):
  def print(self, expr: Expr):
    return expr.accept(self)
  

  def visit_binary(self, binary: Expr.Binary):
    return self.parenthesize(binary.operator.lexeme, binary.left, binary.right)
  

  def visit_grouping(self, grouping: Expr.Grouping):
    return self.parenthesize("group", grouping.expression)
  

  def visit_literal(self, literal: Expr.Literal):
    if literal.value == None: 
      return "nil"
    return str(literal.value)
  

  def visit_unary(self, unary: Expr.Unary):
    return self.parenthesize(unary.operator.lexeme, unary.right)
  
  
  def parenthesize(self, name: str, *exprs: Expr):
    builder = [f"({name}"]
    for e in exprs:
      builder.append(f" {e.accept(self)}")
    builder.append(")")
    return "".join(builder)
  