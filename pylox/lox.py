import sys
from pylox.scanner.scanner import Scanner
from pylox.scanner.token_item import TokenItem
from pylox.scanner.token_type import TokenType

class Lox:
  has_error = False
  
  @staticmethod
  def init() -> None:
    if len(sys.argv) > 2:
      print('Usage pylox [script]')
    elif len(sys.argv) == 2:
      Lox.run_file(sys.argv[1])
    else:
      Lox.run_prompt()


  @staticmethod
  def run_prompt() -> None:
    while True:
      line: str = input('> ')
      if line is None: break
      Lox.run(line)
      Lox.had_error = False


  @staticmethod
  def run_file(path: str) -> None:
    with open(path, 'r', encoding='utf-8') as file:
      contents = file.read()

    Lox.run(contents)

    if Lox.has_error: 
      return


  @staticmethod
  def run(source: str) -> None:
    scanner = Scanner(source, Lox.scanner_error)
    tokens: list[TokenItem] = scanner.scan_tokens()

    for token in tokens:
      print(token)

    # parser = Parser(tokens, Lox.parse_error)

  
  @staticmethod
  def scanner_error(line: int, message: str) -> None:
    Lox.report(line, "", message)

  @staticmethod
  def parse_error(token: TokenItem, message: str) -> None:
    if token.token_type == TokenType.EOF:
      Lox.report(token.line, " at end", message)
    else:
      Lox.report(token.line, " at '" + token.lexeme + "'", message)

  @staticmethod
  def report(line: int, where: str, message: str) -> None:
    print(f'[line {line} ] Error{where}: {message}')

