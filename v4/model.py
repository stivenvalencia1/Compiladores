from collections import deque
from dataclasses import dataclass
from typing  import Callable

@dataclass
class Symbol:
    name: str
    type: str #Tokens tipo var, BLTIN, UNDEF
    val : float = 0.0
    ptr : Callable = None

@dataclass
class LinkedListIterator:
    def __init__(self, symbol):
        self.cur = symbol

    def __iter__(self):
        return self

    def __next__(self):
        if not self.cur:
            raise StopIteration
        else:
            symbol = self.cur
            self.cur = self.cur.next
            return symbol
@dataclass
class LinkedList:
    symbol: Symbol = None

    def __iter__(self):
        return LinkedListIterator(self.symbol)

    def add(self, symbol):
        symbol.next = self.symbol
        self.symbol = symbol

# Definición de Stack
@dataclass
class Stack(deque):
    push = deque.append

    def peek(self):
        return self[-1]


# tipo para interpretar la stack
@dataclass
class Datum:
    val : float = 0.0
    sym : Symbol = None