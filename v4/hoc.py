'''
Nivel 4: Compilación en una Maquina de Pila
'''
from errors import error
from init import *
from model import *
from vm import *

import math
import sly

# =====================================================================
# Analizador Lexico
# =====================================================================
class Lexer(sly.Lexer):

	tokens = {
		NUMBER, VAR, BLTIN,
	}
	literals = '+-*/()=^'

	# patrones para ignorar
	ignore = ' \t'

	@_(r'\n+')
	def ignore_newline(self, t):
		self.lineno += t.value.count('\n')

	# Definición de Tokens

	# variables
	@_(r'[a-zA-Z_][a-zA-Z0-9_]*')
	def VAR(self, t):
		s = lookup(t.value)
		if s is None:
			s = install(t.value, 'UNDEF')
		t.type = 'VAR' if s.type == 'UNDEF' else s.type
		t.value = s
		return t

	# Definir regex para NUMBER
	@_(r'(\d*\.\d+|\d+\.?)([eE][-+]?\d+)?')
	def NUMBER(self, t):
		t.value = install('', 'NUMBER', float(t.value))
		return t

	def error(self, t):
		error("%s Caracter es ilegal '{t.value[0]}'", t.lineno)
		self.index += 1

# =====================================================================
# Analizador Sintático
# =====================================================================
class Parser(sly.Parser):
	debugfile = 'hoc4.txt'

	tokens = Lexer.tokens

	precedence = (
		('right', '='),
		('left', '+', '-'),
		('left', '*', '/'),
		('left', UMINUS),
		('right', '^'),
	)

	# Definición de la gramática
	@_("empty")
	def list(self, p):
		pass

	#@_("list asgn")
	#def list(self, p):
	#	code2(pop, STOP)

	@_("list expr")
	def list(self, p):
		code2(println, STOP)

	@_("list error")
	def list(self, p):
		error(f"error de sintaxis en token")
		self.errok()

	@_("VAR '=' expr")
	def asgn(self, p):
		code3(varpush, p.VAR, assign)

	@_("NUMBER")
	def expr(self, p):
		code2(constpush, p.NUMBER)

	@_("VAR")
	def expr(self, p):
		code3(varpush, p.VAR, eval)

	@_("asgn")
	def expr(self, p):
		pass

	@_("BLTIN '(' expr ')'")
	def expr(self, p):
		code2(bltin, p.BLTIN)

	@_("expr '+' expr")
	def expr(self, p):
		code(add)

	@_("expr '-' expr")
	def expr(self, p):
		code(sub)

	@_("expr '*' expr")
	def expr(self, p):
		code(mul)

	@_("expr '/' expr")
	def expr(self, p):
		code(div)

	@_("expr '^' expr")
	def expr(self, p):
		code(power)

	@_("'(' expr ')'")
	def expr(self, p):
		pass

	@_("'-' expr %prec UMINUS")
	def expr(self, p):
		code(negate)

	@_("")
	def empty(self, p):
		pass

	def error(self, p):
		if p:
			print("Error de sintaxis en token", p.type)
			self.errok()
		else:
			print("Error de sintaxis en EOF")

init()

def main():
	l = Lexer()
	p = Parser()

	while True:
		try:
			text = input('$ ')
			p.parse(l.tokenize(text))
			#mostrarVM()
			execute()
			initcode()
		except EOFError:
			break

if __name__ == '__main__':
	main()
