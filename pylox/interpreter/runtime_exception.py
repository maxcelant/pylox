from pylox.scanner.token_item import TokenItem


class RuntimeException(Exception):
  def __init__(self, token: TokenItem, message: str):
    super().__init__(message)
    self.token = token