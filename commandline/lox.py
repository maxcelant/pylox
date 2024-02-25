import sys
from runtime.scanner.scanner import Scanner
from runtime.scanner.token_item import TokenItem

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

    if Lox.has_error: return


  @staticmethod
  def run(source: str) -> None:
    scanner = Scanner(source, Lox.error)
    tokens: list[TokenItem] = scanner.scan_tokens()

    for token in tokens:
      print(token)

  
  @staticmethod
  def error(line: int, message: str) -> None:
    Lox.report(line, "", message)

  
  @staticmethod
  def report(line: int, where: str, message: str) -> None:
    print(f'[line {line} ] Error{where}: {message}')

