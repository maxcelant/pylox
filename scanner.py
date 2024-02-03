from token import Token
from token_type import TokenType
from lox import Lox


class Scanner:
  def __init__(self, source: string) -> None:
    self.source = source
    self.tokens: list[Token] = []
    self.start = 0
    self.current = 0
    self.line = 1


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
    else:
      Lox.error(self.line, "Unexpected character.")

  
  def match(self, expected: str) -> bool:
    if self.is_at_end(): return False
    if self.source[self.current] != expected: return False
    self.current += 1
    return True

  
  def peek(self) -> str:
    if self.is_at_end():
      return '\0'
    return self.source[self.current] 
  
  
  def is_at_end(self) -> boolean:
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
  
  
