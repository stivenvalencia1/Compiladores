'''
Nivel 3: Variables longitud arbitraria y funciones
'''
from init import *
from model import *
from math import pow
import sly
#mem = {'p':0}    # Tabla de simbolos
# =====================================================================
# Analizador Lexico
# =====================================================================
class Lexer(sly.Lexer):

    tokens = {
        NUMBER, VAR, NEWLINE, BLTIN,
    }
    literals = '+-*/()=%^'

    # patrones para ignorar
    ignore = ' \t'

    # Definición de Tokens
    @_(r'[a-zA-Z_][a-zA-z0-9_]*')
    def VAR(self, t):
        s = lookup(t.value)
        if s is None:
            s = install(t.value, 'UNDEF')
        t.type = 'VAR' if s.type == 'UNDEF' else s.type
        t.value = s
        return t

    # Definir regex para NUMBER
    @_(r'\d*\.\d+|\d+\.?')
    def NUMBER(self, t):
        t.value = float(t.value)
        return t

    def error(self, t):
        print("%s Caracter es ilegal '%s'" % (t.lineno, t.value[0]))
        self.index += 1

    @_(r'\\n|\;')
    def NEWLINE(self, t):
        self.lineno += 1
        return t

# =====================================================================
# Analizador Sintático
# =====================================================================
class Parser(sly.Parser):
    debugfile = 'hoc3.txt'

    tokens = Lexer.tokens

    precedence = (
        ('right', '='),
        ('left', '+', '-'),
        ('left', '*', '/', '%'),
        ('left', UMINUS),
        ('right', '^'),
    )

	# Definición de la gramática
    @_("empty")
    def list(self, p):
        pass

    @_("list asgn")
    def list(self, p):
        pass

    @_("list asgn NEWLINE")
    def list(self, p):
        pass

    @_("list expr")
    def list(self, p):
        return p.expr

    @_("list expr NEWLINE")
    def list(self, p):
        return p.expr

    @_("list error")
    def list(self, p):
        print(f"error de sintaxis en token '{p.type}'")
        self.errok()

    @_("list error NEWLINE")
    def list(self, p):
        print(f"error de sintaxis en token '{p.type}'")
        self.errok()

    @_("VAR '=' expr")
    def asgn(self, p):
        p.VAR.val = p.expr
        p.VAR.type = 'VAR'
        return p

    @_("NUMBER")
    def expr(self, p):
        return p.NUMBER

    @_("VAR")
    def expr(self, p):
        if p.VAR.type == 'UNDEF':
            print(f"Variable '{p.VAR.name}' no esta definida")
        return p.VAR.val

    @_("BLTIN '(' expr ')'")
    def expr(self, p):
        return p.BLTIN.ptr(p.expr)

    @_("expr '+' expr")
    def expr(self, p):
        return p.expr0 + p.expr1

    @_("expr '-' expr")
    def expr(self, p):
        return p.expr0 - p.expr1

    @_("expr '*' expr")
    def expr(self, p):
        return p.expr0 * p.expr1

    @_("expr '/' expr")
    def expr(self, p):
        try:
            return p.expr0 / p.expr1
        except ZeroDivisionError:
            return float('inf')

    @_("expr '%' expr")
    def expr(self, p):
        try:
            return p.expr0 % p.expr1
        except ZeroDivisionError:
            return float('inf')

    @_("expr '^' expr")
    def expr(self, p):
        return pow(p.expr0, p.expr1)

    @_("'(' expr ')'")
    def expr(self, p):
        return p.expr

    @_("'-' expr %prec UMINUS")
    def expr(self, p):
        return -p.expr

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
            result = p.parse(l.tokenize(text))
            if isinstance(result,float):
                print("\t%.8g" % result)
        except EOFError:
            break

if __name__ == '__main__':
    main()