
from pylox.parser.productions import Expr
from pylox.scanner.token_item import TokenItem
from pylox.scanner.token_type import TokenType


class Parser:
  def __init__(self, tokens: list[TokenItem]):
    self.tokens  = tokens
    self.current = 0

  def match(self, *types: TokenType) -> bool:
    for t in types:
      if self.check(t):
        self.advance()
        return True
    return False
  
  def check(self, token_type: TokenType) -> bool:
    if self.is_at_end():
      return False
    return self.peek().token_type == token_type

  def advance(self) -> TokenItem:
    if not self.is_at_end():
      self.current += 1
    return self.previous()
  
  def is_at_end(self) -> bool:
    return self.peek().token_type == TokenType.EOF
  
  def peek(self) -> TokenItem:
    return self.tokens[self.current]
  
  def previous(self) -> TokenItem:
    return self.tokens[self.current - 1]
  
  def expression(self) -> Expr:
    return self.equality()
  
  def equality(self) -> Expr:
    expr: Expr = self.comparison()

    while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
      operator: TokenItem = self.previous()
      right: Expr = self.comparison()
      expr = Expr.Binary(expr, operator, right)

    return expr