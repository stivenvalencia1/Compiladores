# model.py
from collections import deque
from dataclasses import dataclass
from typing import Callable


# Entrada a la tabla de simbolos
@dataclass
class Symbol:
	name: str
	type: str  # VAR, BLTIN, UNDEF
	val : float = 0.0 
	ptr : Callable = None


# Tabla de Simbolos
@dataclass
class LinkedListIterator:
	cur : Symbol

	def __iter__(self):
		return self

	def __next__(self):
		if not self.cur:
			raise StopIteration
		else:
			sym = self.cur
			self.cur = self.cur.next 
			return sym

@dataclass
class LinkedList:
	sym : Symbol = None

	def __iter__(self):
		return LinkedListIterator(self.sym)

	def add(self, sym):
		sym.next = self.sym 
		self.sym = sym 


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
