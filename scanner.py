from token import Token


class Scanner:
  def __init__(self, source: string):
    self.__source = source
    self.__tokens: list[Token] = []
    self.__start = 0
    self.__current = 0
    self.__line = 1

  def scan_tokens():
    while not at_end:
      self.__start = self.__current
      scan_token()

    self.__tokens.append(Token(token_type=TokenType.EOF, lexeme="", literal=None, line=self.__line))
    return tokens