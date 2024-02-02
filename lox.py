import sys

class Lox:
  has_error = False
  
  @staticmethod
  def main():
    if len(sys.argv) > 1:
      print('Usage pylox [script]')
    elif len(sys.argv) == 1:
      Lox.run_file(sys.argv[0])
    else:
      Lox.run_prompt()


  @staticmethod
  def run_prompt():
    while True:
      line: str = input('> ')
      if line is None: break
      Lox.run(line)
      Lox.had_error = False

  @staticmethod
  def run_file(path: str):
    with open(path, 'r', encoding='utf-8') as file:
      contents = file.read()

    Lox.run(contents)

    if Lox.had_error: return


  @staticmethod
  def run(source: str):
    scanner = Scanner(source)
    tokens: list[Token] = scanner.scanTokens()

    for token in tokens:
      print(token)

  @staticmethod
  def error(line: int, message: str):
    Lox.report(line, "", message)


  def report(line: int, where: str, message: str):
    print(f'[line {line} ] Error{where}: {message}')


if __name__ == '__main__':
  main()

