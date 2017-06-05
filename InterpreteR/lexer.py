import ply.lex as lex
import re
import codecs
import os
import sys

# -----------------------------
# R.py
# -----------------------------

literals =  [ '?', '~', '+', '-', '*', '/', ':', ';', '!', '$', '@', '[', ']', '(', ')', '{', '}', ',' ]

## ----------------------------------------------------------------------------------------

reserved = {
    'si':'IF', 'sino':'ELSE', 'mientras':'WHILE', 'para':'FOR',
    'en':'IN', 'funcion':'FUNCTION', 'verdadero':'TRUE', 'falso':'FALSE',
    'nulo':'NULL_CONST', 'infinito':'Inf', 'noNumero':'NaN', 'noDisponible':'NA'
}

## ----------------------------------------------------------------------------------------

tokens = [
    'REAL', 'INT', 'STR_CONST', 'SYMBOL', 'LEFT_ASSIGN', 'EQ_ASSIGN', 'RIGHT_ASSIGN',
    'LBB', 'GT', 'GE', 'LT', 'LE', 'EQ', 'NE', 'AND', 'OR', 'AND2', 'OR2',
    'NLINE', 'MOD', 'INT_DIV', 'COMMENT', 'MATRIX_MULT', 'POWER'
]
tokens += reserved.values()

## ----------------------------------------------------------------------------------------

# Ignored characters
t_ignore_COMMENT = r'\#.*'
t_ignore = ' \t\r'

# Constants

t_STR_CONST = r'(\"[^\"]*\")|(\'[^\']*\')'
t_INT = r'\d+'
t_REAL = r'(\d+(\.\d*)?|\.\d+)([eE][-+]? \d+)?'


#Operators
t_GT = r'>'
t_GE = r'>='
t_LT = r'<'
t_LE = r'<='
t_EQ = r'=='
t_NE = r'!='
t_AND = r'&'
t_OR = r'\|'
t_AND2 = r'&&'
t_OR2 = r'\|\|'
t_EQ_ASSIGN = r'='
t_POWER = r'(\^)|(\*\*)'
t_INT_DIV = r'%/%'
t_MOD = r'%%'
t_MATRIX_MULT = r'%*%'
t_LEFT_ASSIGN = r'<-'
t_RIGHT_ASSIGN = r'->'
t_LBB = r'\[\['



def t_SYMBOL(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'SYMBOL')
    return t


def t_newline(t):
    r'\n'
    t.lexer.lineno += 1
    t.type = "NLINE"
    return t
    
def t_error(t):
    print("Caracter ilegal '" + t.value[0] + "' en la linea " , str(t.lineno))
    t.lexer.skip(1)
    
# Construir el lexer
lexer = lex.lex()


# def buscarFicheros(directorio):
#     ficheros = []
#     numArchivo = ''
#     respuesta = False
#     cont = 1

#     for base, dirs, files in os.walk(directorio):
#         ficheros.append(files)

#     for file in files:
#         print(str(cont)+". "+str(file))
#         cont = cont+1

#     while respuesta== False:
#         numArchivo = input('\nNumero del test: ')
#         for file in files:
#             if file == files[int(numArchivo)-1]:
#                 respuesta = True
#                 break

#     print('Has escogido \"%s\"\n' %(files[int(numArchivo)-1]))
    
#     return files[int(numArchivo)-1]

# directorio = 'C:/Users/Andrey/Documents/Git/Compiladores/InterpreteR/Tests/'
# archivo = buscarFicheros(directorio)
# test = directorio+archivo
# fp = codecs.open(test,"r","utf-8")
# cadena = fp.read()
# fp.close()

# lexer = lex.lex()

# lexer.input(cadena)

# while True:
#     tok = lexer.token()
#     if not tok : break
#     print (tok)



