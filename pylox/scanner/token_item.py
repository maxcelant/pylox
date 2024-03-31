from pylox.scanner.token_type import TokenType

class TokenItem:
  def __init__(self, token_type: TokenType, lexeme: str, literal: object, line: int):
    self.token_type = token_type
    self.lexeme = lexeme
    self.literal = literal
    self.line = line


  def __repr__(self):
    return f'Token({self.token_type.name=}, {self.lexeme=}, {self.literal=})'
