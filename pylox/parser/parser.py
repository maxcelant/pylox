
from typing import Callable
from pylox.parser.expr import Expr
from pylox.parser.stmt import Stmt
from pylox.scanner.token_item import TokenItem
from pylox.scanner.token_type import TokenType


class Parser:

  class ParseError(Exception):
    pass

  def __init__(self, tokens: list[TokenItem], error_callback: Callable[[int, str], None]):
    self.tokens = tokens
    self.error_callback = error_callback
    self.current = 0


  def parse(self) -> list[Stmt]:
    statements: list[Stmt] = []
    while not self.is_at_end():
      statements.append(self.declaration())
    return statements
  

  def declaration(self) -> Stmt:
    try:
      if self.match(TokenType.VAR):
        return self.var_declaration()
      return self.statement()
    except Parser.ParseError:
      self.synchronize()
      return None
    
  
  def statement(self) -> Stmt:
    if self.match(TokenType.IF):
      return self.if_statement()
    if self.match(TokenType.PRINT):
      return self.print_statement()
    if self.match(TokenType.WHILE):
      return self.while_statement()
    if self.match(TokenType.LEFT_BRACE):
      return Stmt.Block(self.block())
    return self.expression_statement()
  
  def var_declaration(self) -> Stmt:
    name: TokenItem = self.consume(TokenType.IDENTIFIER, "Expect variable name.")

    initializer: Expr = None
    if self.match(TokenType.EQUAL):
      initializer = self.expression()
    
    self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
    return Stmt.Var(name, initializer)
  

  def while_stmt(self) -> Stmt:
    self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
    condition: Expr = self.expression()
    self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
    body: Stmt = self.statement()

    return Stmt.While(condition, body)


  def if_statement(self) -> Stmt:
    self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
    condition: Expr = self.expression()
    self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

    then_branch: Stmt = self.statement()
    else_branch: Stmt | None = self.statement() if self.match(TokenType.ELSE) else None
    
    return Stmt.If(condition, then_branch, else_branch) 


  def print_statement(self) -> Stmt:
    value: Expr = self.expression()
    self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
    return Stmt.Print(value)
  

  def block(self) -> list[Stmt]:
    statements: list[Stmt] = []

    while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
      statements.append(self.declaration())

    self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
    return statements


  def expression_statement(self) -> Stmt:
    expr: Expr = self.expression()
    self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
    return Stmt.Expression(expr)
  

  def expression(self) -> Expr:
    return self.assignment()
  

  def assignment(self) -> Expr:
    expr: Expr = self.logic_or()

    if self.match(TokenType.EQUAL):
      equals: TokenItem = self.previous()
      value: Expr = self.assignment()

      if isinstance(expr, Expr.Variable):
        name: TokenType = expr.name
        return Expr.Assign(name, value)
      
      self.error(equals, "Invalid assignment target.")
    
    return expr
  

  def logic_or(self) -> Expr:
    expr: Expr = self.logic_and()

    while self.match(TokenType.OR):
      operator: TokenType = self.previous()
      right: Expr = self.logic_and()
      expr = Expr.Logical(expr, operator, right)

    return expr
  

  def logic_and(self) -> Expr:
    expr: Expr = self.equality()

    while self.match(TokenType.AND):
      operator: TokenType = self.previous()
      right: Expr = self.equality()
      expr = Expr.Logical(expr, operator, right)

    return expr
  
  def equality(self) -> Expr:
    expr: Expr = self.comparison()

    while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
      operator: TokenItem = self.previous()
      right: Expr = self.comparison()
      expr = Expr.Binary(expr, operator, right)

    return expr


  def comparison(self) -> Expr:
    expr: Expr = self.term()

    while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
      operator: TokenItem = self.previous()
      right: Expr = self.term()
      expr = Expr.Binary(expr, operator, right)
    
    return expr


  def term(self) -> Expr:
    expr: Expr = self.factor()

    while self.match(TokenType.MINUS, TokenType.PLUS):
      operator: TokenItem = self.previous()
      right: Expr = self.factor()
      expr = Expr.Binary(expr, operator, right)
    
    return expr


  def factor(self) -> Expr:
    expr: Expr = self.unary()

    while self.match(TokenType.SLASH, TokenType.STAR):
      operator: TokenItem = self.previous()
      right: Expr = self.unary()
      expr = Expr.Binary(expr, operator, right)

    return expr


  def unary(self) -> Expr:
    if self.match(TokenType.BANG, TokenType.MINUS):
      operator: TokenItem = self.previous()
      right: Expr = self.unary()
      return Expr.Unary(operator, right)

    return self.primary()


  def primary(self) -> Expr:
    if self.match(TokenType.FALSE): return Expr.Literal(False)
    if self.match(TokenType.TRUE): return Expr.Literal(True)
    if self.match(TokenType.NIL): return Expr.Literal(None)

    if self.match(TokenType.NUMBER, TokenType.STRING):
      return Expr.Literal(self.previous().literal)
    
    if self.match(TokenType.IDENTIFIER):
      return Expr.Variable(self.previous())
    
    if self.match(TokenType.LEFT_PAREN):
      expr: Expr = self.expression()
      self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression")
      return Expr.Grouping(expr)
    
    raise self.error_callback(self.peek(), "Expect expression.")


  def match(self, *types: TokenType) -> bool:
    for t in types:
      if self.check(t):
        self.advance()
        return True
    return False
  

  def consume(self, token_type: TokenType, message: str) -> TokenItem:
    if self.check(token_type):
      return self.advance()
    raise self.error(self.peek(), message)
  

  def check(self, token_type: TokenType) -> bool:
    if self.is_at_end():
      return False
    return self.peek().token_type == token_type


  def advance(self) -> TokenItem:
    if not self.is_at_end():
      self.current += 1
    return self.previous()


  def is_at_end(self) -> bool:
    return self.peek().token_type == TokenType.EOF


  def peek(self) -> TokenItem:
    return self.tokens[self.current]


  def previous(self) -> TokenItem:
    return self.tokens[self.current - 1]


  def error(self, token: TokenItem, message: str):
    self.error_callback(token, message)
    return Parser.ParseError()


  def synchronize(self) -> None:
    self.advance()

    while not self.is_at_end():
      if self.previous().token_type == TokenType.SEMICOLON:
        return

      if self.peek().token_type in {
        TokenType.CLASS,
        TokenType.FUN,
        TokenType.VAR,
        TokenType.FOR,
        TokenType.IF,
        TokenType.WHILE,
        TokenType.PRINT,
        TokenType.RETURN,
      }:
        return
      
      self.advance()