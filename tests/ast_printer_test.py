from pylox.parser.ast_printer import AstPrinter
from pylox.parser.productions import Expr
from pylox.scanner.token_item import TokenItem
from pylox.scanner.token_type import TokenType


def main():
  expression = Expr.Binary(
    Expr.Unary(TokenItem(TokenType.MINUS, "-", None, 1), Expr.Literal(123)),
    TokenItem(TokenType.STAR, "*", None, 1),
    Expr.Grouping(Expr.Literal(45.67))
  )
  print(AstPrinter().print(expression))


if __name__ == '__main__':
  main()