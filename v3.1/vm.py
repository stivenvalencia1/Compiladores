# vm.py
from errors import execerror
from math import pow
from model import *

# Definición de la Maquina
NSTACK = 256
stack = Stack()

NPROG = 2000
prog  = []
pc    = 0

STOP  = None

def initcode():
	global stack, prog
	stack = Stack()
	prog  = []

def execute(p:int=0):
	global pc
	pc = p
	while prog[pc] is not STOP:
		if isinstance(prog[pc], int): pc = prog[pc]
		ir = prog[pc]; pc += 1
		ir()

def code(f):
	if len(prog) >= NPROG:
		execerror("programa es muy grande")
	prog.append(f)
	return len(prog) - 1

def code2(c1, c2):
	ret = code(c1); code(c2)
	return ret

def code3(c1, c2, c3):
	ret = code(c1); code(c2); code(c3)
	return ret

def push(d: Datum):
	if len(stack) >= NSTACK:
		execerror("desbordamiento de la pila")
	stack.push(d)

def pop() -> Datum:
	if len(stack) == 0:
		execerror("desbordamiento de la pila")
	return stack.pop()

# ALU - Operaciones de la Maquina
def constpush():
	global pc
	d = Datum(val=prog[pc].val); pc += 1
	push(d)

# agregar una variable a la pila
def varpush():
	global pc
	d = Datum(sym=prog[pc]); pc += 1
	push(d)

# evaluar bultin en top de la pila
def bltin():
	global pc
	d = pop()
	d.val = prog[pc].ptr(d.val); pc += 1
	push(d)

# evluar una variable en la pila
def eval():
	d = pop()
	if d.sym.type == 'UNDEF':
		execerror(f"variable indefinida {d.sym.name}")
	d.val = d.sym.val
	push(d)

# add dos valores de la pila
def add():
	d2 = pop()
	d1 = pop()
	d1.val += d2.val 
	push(d1)

# sub dos valores de la pila
def sub():
	d2 = pop()
	d1 = pop()
	d1.val -= d2.val 
	push(d1)

# mul dos valores de la pila
def mul():
	d2 = pop()
	d1 = pop()
	d1.val *= d2.val 
	push(d1)

# div dos valores de la pila
def div():
	d2 = pop()
	if d2.val == 0.0:
		execerror("division por cero")
	d1 = pop()
	d1.val /= d2.val 
	push(d1)

# mod dos valores de la pila
def mod():
	d2 = pop()
	d1 = pop()
	d1.val %= d2.val 
	push(d1)

# negate dos valores de la pila
def negate():
	d = pop()
	d.val = -d.value
	push(d1)

# power dos valores de la pila
def power():
	d2 = pop()
	d1 = pop()
	d1.val = pow(d1.val, d2.val)
	push(d1)

# asignacion
def assign():
	d1 = pop()
	d2 = pop()
	if d1.sym.type != 'VAR' and d1.sym.type != 'UNDEF':
		execerror(f"asignacion a no variable {d1.sym.name}")
	d1.sym.val  = d2.val
	d1.sym.type = 'VAR'
	push(d2)

# imprimir
def println():
	d = pop()
	print("\t%.8g" % d.val)

def mostrarVM():
	for p in prog:
		if type(p) == Symbol:
			if p.type == "NUMBER":
				print(p.val)
			else:
				print(p.name)
		else:
			print(p)
