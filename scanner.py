from token import Token
from lox import Lox


class Scanner:
  def __init__(self, source: string) -> None:
    self.source = source
    self.tokens: list[Token] = []
    self.start = 0
    self.current = 0
    self.line = 1

  def is_at_end(self) -> boolean:
    return self.current >= len(self.source)

  def scan_tokens(self) -> list[Token]:
    while not self.is_at_end():
      self.start = self.current
      self.scan_token()

    self.tokens.append(Token(token_type=TokenType.EOF, lexeme="", literal=None, line=self.line))
    return tokens

  def scan_token(self) -> None:
    c = self.advance()
    if c == '(':
      self.add_token(TokenType.LEFT_PAREN)
    elif c == ')':
      self.add_token(TokenType.RIGHT_PAREN)
    elif c == '{':
      self.add_token(TokenType.LEFT_BRACE)
    elif c == '}':
      self.add_token(TokenType.RIGHT_BRACE)
    elif c == ",":
      self.add_token(TokenType.COMMA)
    elif c == ".":
      self.add_token(TokenType.DOT)
    elif c == "-":
      self.add_token(TokenType.MINUS)
    elif c == "+":
      self.add_token(TokenType.PLUS)
    elif c == ";":
      self.add_token(TokenType.SEMICOLON)
    elif c == "*":
      self.add_token(TokenType.STAR)
    else:
      Lox.error(self.line, "Unexpected character.")

  def advance(self) -> str:
    self.current += 1
    return self.source[self.current]

  def add_token(self, token_type: TokenType) -> None:
    self.add_token(token_type, None)

  def add_token(self, token_type: TokenType, literal: object) -> None:
    text = self.source[self.start:self.current]
    self.tokens.append(Token(token_type=token_type, lexeme=text, literal=literal, line=self.line))