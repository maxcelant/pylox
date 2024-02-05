from typing import Callable

from token import Token
from token_type import TokenType


class Scanner:
  def __init__(self, source: str, error_callback: Callable[[int, str], None]) -> None:
    self.source = source
    self.error_callback = error_callback
    self.tokens: list[Token] = []
    self.start = 0
    self.current = 0
    self.line = 1
    self.keywords = {
      "and": TokenType.AND,
      # Continue here
    }


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
    elif c == '!':
      self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
    elif c == '=':
      self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
    elif c == '<':
      self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
    elif c == '>':
      self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
    elif c == '/':
      if self.match('/'):
        while self.peek() != '\n' and not self.is_at_end():
          self.advance()
      else:
        add_token(TokenType.SLASH)
    elif c == ' ' or c == '\r' or c == '\t':
      pass
    elif c == '\n':
      self.line += 1
    elif c == '"':
      self.string()
    elif self.is_digit(c):
      self.number()
    elif c == 'o':
      if self.match('r'):
        self.add_token(token_type=TokenType.OR)
    elif self.is_alpha(c):
      self.identifier()
    else:
      self.error_callback(self.line, "Unexpected character.")

  
  def identifier(self) -> None:
    while self.is_alphanumeric(self.peek()):
      self.advance()

    self.add_token(token_type=TokenType.IDENTIFIER)

  def number(self) -> None:
    while self.is_digit(self.peek()):
      self.advance()

    # Look for a fractional part
    if self.peek() == '.' and self.is_digit(self.peek_next()):
      self.advance() # Consume the "."

      while self.is_digit(self.peek()):
        self.advance()

    self.add_token(token_type=TokenType.NUMBER, literal=float(source[start:current]))


  def string(self) -> None:
    while self.peek() != '"' and not self.is_at_end():
      if self.peek() == '\n': self.line += 1
      self.advance()
    
    if self.is_at_end():
      self.error_callback(self.line, "Unterminated string.")
      return

    self.advance() # Closing ".

    value: str = self.source[self.start + 1: self.current - 1]
    self.add_token(token_type=TokenType.STRING, literal=value)

  
  def match(self, expected: str) -> bool:
    if self.is_at_end(): 
      return False
    if self.source[self.current] != expected: 
      return False
    self.current += 1
    return True

  
  def peek(self) -> str:
    if self.is_at_end():
      return '\0'
    return self.source[self.current]

  
  def peek_next(self) -> str:
    if self.current + 1 >= len(self.source):
      return '\0'
    return self.source[current + 1]

  
  def is_alpha(self, c: str) -> bool:
    return (c >= 'a' and c <= 'z') or \
           (c >= 'A' and c <= 'Z') or \
           (c == '_')

  
  def is_alphanumeric(self, c: str) -> bool:
    return self.is_alpha(c) or self.is_digit()

  
  def is_digit(self, c :str) -> bool:
    return c >= '0' and c <= '9'
  
  
  def is_at_end(self) -> bool:
    return self.current >= len(self.source)


  def advance(self) -> str:
    c = self.source[self.current]
    self.current += 1
    return c


  def add_token(self, token_type: TokenType) -> None:
    self.add_token(token_type, None)


  def add_token(self, token_type: TokenType, literal: object) -> None:
    text = self.source[self.start:self.current]
    self.tokens.append(Token(token_type=token_type, lexeme=text, literal=literal, line=self.line))
  
  
