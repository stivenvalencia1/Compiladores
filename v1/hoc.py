'''
Nivel 1: Una calculadora con 4 operaciones

Gramática libre de contexto ()

list : <empty>
    | list expr
    ;

expr : NUMBER
    | expr '+' expr
    | expr '-' expr
    | expr '*' expr
    | expr '/' expr
    | '(' expr ')'
    ;
'''
import sly
class Lexer(sly.Lexer):
    tokens = {NUMBER,NEWLINE,}
    literals = '+-*/()%'
    #Patrones que se pueden igorar
    ignore = ' \t'
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')


    NEWLINE = r'\\n'

    #Definir expresion de NUMBER
    @_(r'\d*\.\d+|\d+\.?')
    def NUMBER(self, t):
        t.value = float(t.value)
        return t

    #Definir manejo de errores
    def error(self, t):
        print("%s Caracter ilegal '%s'" % (t.lineno, t.value[0]))
        self.index += 1

class Parser(sly.Parser):
    debugfile = 'hoc1.txt'
    tokens = Lexer.tokens
    precedence = (
        ('left','+','-'),
        ('left', '*', '/'),
        ('left', '%'),
        ('left', UMINUS)
    )


    @_("empty")
    def list(self, p):
        pass
    @_("list expr")
    def list(self, p):
        return p.expr

    @_("NUMBER")
    def expr(self, p):
        return p.NUMBER
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
        return p.expr0 / p.expr1
    @_("'(' expr ')'")
    def expr(self, p):
        return p.expr

    @_("'-' expr %prec UMINUS")
    def expr(self, p):
        return -p.expr

    @_("expr '%' expr")
    def expr(self, p):
        return p.expr0 % p.expr1
    @_("expr NEWLINE")
    def expr(self, p):
        return p.expr

    @_("")
    def empty(self, p):
        pass
    def error(self, p):
        if p:
            print("Error de sintaxis en token", p.type)
        else:
            print("Error de sintaxis en EOF")


def main():
    lexer = Lexer()
    parser = Parser()
    while True:
        try:
            text = input('$ ')
            result = parser.parse(lexer.tokenize(text))
            print("\t%.8g" % result)
        except EOFError:
            break
if __name__=='__main__':
    main()