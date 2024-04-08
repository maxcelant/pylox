# PyLox

A fully functioning programming language written in Python.

Check out the `/docs` for more info on each portion of the project (scanner, parser and interpreter, etc).

### How to Run

```bash
> python3 main.py [file].lox
```

You can do basic calculations

```ruby
var x = 21 * (12 + (9 / 3))
var y = "foo" + "bar"

print x     // 315
print y     // "foobar"
```

Variable declarations and assignments:

```ruby
var a = 5;
var b;

a = b = 10;

print a; // 10
print b; // 10
```

Lexical Scoping:

```ruby
var a = 5;

{
  var a = 15;
  var b = 10;

  print b;     // 10
  print a;     // 15

  {
    var c = "Hello";
    print c;     // "Hello"
  }
}

print a;    // 5
```
