import time
from pylox.interpreter.lox_callable import LoxCallable


class ClockFunction(LoxCallable):
    def arity(self):
        return 0

    def call(self, interpreter, arguments):
        return time.time()

    def __str__(self):
        return "<native fn>"
