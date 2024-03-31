from pylox.parser.expr import Expr


class AstPrinter(Expr.Visitor):
  def print(self, expr: Expr):
    return expr.accept(self)
  

  def visit_binary_expr(self, binary: Expr.Binary):
    return self.parenthesize(binary.operator.lexeme, binary.left, binary.right)
  

  def visit_grouping_expr(self, grouping: Expr.Grouping):
    return self.parenthesize("group", grouping.expression)
  

  def visit_literal_expr(self, literal: Expr.Literal):
    if literal.value == None: 
      return "nil"
    return str(literal.value)
  

  def visit_unary_expr(self, unary: Expr.Unary):
    return self.parenthesize(unary.operator.lexeme, unary.right)
  
  
  def parenthesize(self, name: str, *exprs: Expr):
    builder = [f"({name}"]
    for e in exprs:
      builder.append(f" {e.accept(self)}")
    builder.append(")")
    return "".join(builder)
  
