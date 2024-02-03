from token_type import TokenType

class Token:
  def __init__(self, token_type: TokenType, lexeme: str, literal: object, line: int):
    self.token_type = token_type
    self.lexem = lexeme
    self.literal = literal
    self.line = line


  def __str__(self):
    return f'{self.token_type} {lexeme} {literal}'
