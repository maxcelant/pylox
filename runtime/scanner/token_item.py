from runtime.scanner.token_type import TokenType

class TokenItem:
  def __init__(self, token_type: TokenType, lexeme: str, literal: object, line: int):
    self.token_type = token_type
    self.lexeme = lexeme
    self.literal = literal
    self.line = line


  def __str__(self):
    return f'token={self.token_type}\nlexeme=\'{self.lexeme}\'\n{f"literal={self.literal}" if self.literal != None else ""}\n'
