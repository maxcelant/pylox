import sys
from pylox.interpreter.interpreter import Interpreter
from pylox.parser.ast_printer import AstPrinter
from pylox.parser.parser import Parser
from pylox.scanner.scanner import Scanner
from pylox.scanner.token_item import TokenItem
from pylox.scanner.token_type import TokenType
from pylox.interpreter.runtime_exception import RuntimeException

class Lox:
  had_error = False
  had_runtime_error = False
  interpreter = None
  
  @staticmethod
  def init() -> None:
    if len(sys.argv) > 2:
      print('Usage pylox [script]')
      return
    
    Lox.interpreter = Interpreter(Lox.runtime_error)
    if len(sys.argv) == 2:
      Lox.run_file(sys.argv[1])
    else:
      Lox.run_prompt()

  @staticmethod
  def run_prompt() -> None:
    while True:
      line: str = input('> ')
      if line is None: 
        break
      Lox.run(line)
      Lox.had_error = False

  @staticmethod
  def run_file(path: str) -> None:
    with open(path, 'r', encoding='utf-8') as file:
      contents = file.read()

    Lox.run(contents)

    if Lox.had_error: 
      sys.exit(65)
    if Lox.had_runtime_error:
      sys.exit(70)

  @staticmethod
  def run(source: str) -> None:
    scanner = Scanner(source, Lox.scanner_error)
    tokens: list[TokenItem] = scanner.scan_tokens()

    parser = Parser(tokens, Lox.parse_error)

    expression = parser.parse()

    print(AstPrinter().print(expression))

    if Lox.had_error:
      return

    Lox.interpreter.interpret(expression)
  
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
  def runtime_error(error: RuntimeException) -> None:
    print(f'Error: {error}\n[line {error.token.line}]') 
    Lox.had_runtime_error = True

  @staticmethod
  def report(line: int, where: str, message: str) -> None:
    print(f'[line {line} ] Error{where}: {message}')

