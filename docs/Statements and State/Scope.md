- **Lexical scope (or static scope)** is a style of scope where the program shows where the scope starts and ends.
- In Lox, curly-braces control scope. 

## Simple implementation of Block Scope

1. As we visit statements in a block, keep track of variables declared.
2. When the last statement is executed, tell the environment to delete all those variables.

## Environment Chaining
- We define a fresh environment for each block containing only variables defined in that scope.
- We need to chain environments together. Because inner scopes should still have reference to variables in outer scopes.
- Start with innermost scope and go out until we find the variable. 

> ![[Pasted image 20240407212405.png]]

## Environment Class Update

- Each environment will have a reference to the scope that wraps it. So checking the `enclosing` is like going up!

```python
class Environment:
  def __init__(self, enclosing: Environment | None = None):
    self.values = {}
    self.enclosing = enclosing            # Nested environment

  def get(self, name: TokenItem):
    if name.lexeme in self.values:
      return self.values[name.lexeme]
    if self.enclosing:
      return self.enclosing.get(name)     # Check nested environment
    
    raise RuntimeException(name, f"...")
```

## Block Syntax and Semantics

We are going to add to the [[Statement Grammar]].

```c
declaration → varDecl | statement ;

statement → exprStmt | printStmt | block ;

block → "{" declaration* "}"
```

**Blocking Scope**

```python
  def execute_block(self, statements, environment):
    previous = self.environment
    try:
      self.environment = environment
      for stmt in statements:
        self.execute(stmt)
    finally:
      self.environment = previous
```

When executing a block of code, the environment represents the _current_ one. Then it resets once the block is done, getting rid of those variables.