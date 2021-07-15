'''
Nivel 2: Variables y recuperación de errores
'''
import sly


mem = {'p':0}    # Tabla de simbolos

# =====================================================================
# Analizador Lexico
# =====================================================================
class Lexer(sly.Lexer):

    tokens = {
        NUMBER, VAR, NEWLINE,
    }
    literals = '+-*/()=%'

    # patrones para ignorar
    ignore = ' \t'

    # Definición de Tokens
    VAR = r'[a-z]'

    # Definir regex para NUMBER
    @_(r'\d*\.\d+|\d+\.?')
    def NUMBER(self, t):
        t.value = float(t.value)
        return t

    def error(self, t):
        print("%s Caracter es ilegal '%s'" % (t.lineno, t.value[0]))
        self.index += 1

    @_(r'\n|\\n|\;')
    def NEWLINE(self, t):
        self.lineno += 1
        return t

# =====================================================================
# Analizador Sintático
# =====================================================================
class Parser(sly.Parser):
    debugfile = 'hoc2.txt'

    tokens = Lexer.tokens

    precedence = (
        ('right', '='),
        ('left', '+', '-'),
        ('left', '*', '/','%'),
        ('left', UMINUS),
    )

	# Definición de la gramática
    @_("empty")
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

    @_("NUMBER")
    def expr(self, p):
        return p.NUMBER

    @_("VAR")
    def expr(self, p):
        return mem[p.VAR]

    @_("VAR '=' expr")
    def expr(self, p):
        mem[p.VAR] = p.expr
        mem['p']=p.expr
        return p.expr

    @_("expr '+' expr")
    def expr(self, p):
        mem['p']=p.expr0 + p.expr1
        return p.expr0 + p.expr1

    @_("expr '-' expr")
    def expr(self, p):
        mem['p']=p.expr0 - p.expr1
        return p.expr0 - p.expr1

    @_("expr '*' expr")
    def expr(self, p):
        mem['p']=p.expr0 * p.expr1
        return p.expr0 * p.expr1

    @_("expr '/' expr")
    def expr(self, p):
        try:
            mem['p']=p.expr0 / p.expr1
            return p.expr0 / p.expr1
        except ZeroDivisionError:
            return float('inf')

    @_("expr '%' expr")
    def expr(self, p):
        try:
            mem['p']=p.expr0 % p.expr1
            return p.expr0 % p.expr1
        except ZeroDivisionError:
            return float('inf')

    @_("'(' expr ')'")
    def expr(self, p):
        return p.expr

    @_("'-' expr %prec UMINUS")
    def expr(self, p):
        mem['p']=-p.expr
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


def main():
    l = Lexer()
    p = Parser()

    while True:
        try:
            text = input('$ ')
            result = p.parse(l.tokenize(text))
            print("\t%.8g" % result)
        except EOFError:
            break

if __name__ == '__main__':
    main()