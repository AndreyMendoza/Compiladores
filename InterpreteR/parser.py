import ply.yacc as yacc
import os
import codecs
import re
from lexer import tokens
from sys import stdin 



precedence = (
    ('left', '?'),
    ('left', 'LOW','WHILE','FOR'),
    ('right', 'IF'),
    ('left', 'ELSE'),
    ('right', 'LEFT_ASSIGN'),
    ('right', 'EQ_ASSIGN'),
    ('left', 'RIGHT_ASSIGN'),
    ('left', '~', 'TILDE'),
    ('left', 'OR', 'OR2'),
    ('left', 'AND', 'AND2'),
    ('left', 'UNOT', '!'),
    ('nonassoc', 'GT', 'GE', 'LT', 'LE', 'EQ', 'NE'),
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('left', 'MOD', 'INT_DIV', 'MATRIX_MULT'),
    ('left', ':'),
    ('left', 'UMINUS'),
    ('right', 'POWER'),
    ('left', '$', '@'),
    ('nonassoc', '(', '[', 'LBB')
)


## ---------------------------------------------------------------------------------------------------------------------

def p_prog_start(p):
    """prog : exprlist"""
    p[0] = ('prog', p[1])

## ---------------------------------------------------------------------------------------------------------------------

def p_emptyline(p):
    """emptyline : NLINE
                 | emptyline NLINE"""
    pass

## ---------------------------------------------------------------------------------------------------------------------

def p_exprlist_1(p):
    """exprlist : empty
                | expr_or_assign"""
    p[0] = []
    if p[1] is not None: p[0].append(p[1])

def p_exprlist_2(p):
    """exprlist : exprlist ';'
                | exprlist emptyline"""
    p[0] = p[1]

def p_exprlist_3(p):
    """exprlist : exprlist ';' expr_or_assign
                | exprlist emptyline expr_or_assign"""
    p[0] = p[1]
    p[0].append(p[3])

## ---------------------------------------------------------------------------------------------------------------------

def p_expr_or_assign_1(p):
    """expr_or_assign : expr"""
    p[0] = p[1]

def p_expr_or_assign_2(p):
    """expr_or_assign : SYMBOL EQ_ASSIGN expr_or_assign"""
    p[0] = ('call', 'exec_assign', [p[1], p[3]])

def p_expr_or_assign_nl_1(p):
    """expr_or_assign_nl : expr_or_assign"""
    p[0] = p[1]

def p_expr_or_assign_nl_2(p):
    """expr_or_assign_nl : emptyline expr_or_assign"""
    p[0] = p[2]

## ---------------------------------------------------------------------------------------------------------------------

def p_expr_1(p):
    """expr : const_or_symbol
            | binary_operation
            | unary_operation
            | statement_declaration"""
    p[0] = p[1]

def p_expr_2(p):
    """expr : expr RIGHT_ASSIGN SYMBOL
            | SYMBOL LEFT_ASSIGN expr """
    if p[2] == '<-':
        p[0] = ('call', 'exec_assign', [p[1], p[3]])
    else:
        p[0] = ('call', 'exec_assign', [p[3], p[1]])

def p_expr_3(p):
    """expr : '(' expr_or_assign ')'"""
    p[0] = p[2]

def p_expr_4(p):
    """expr : expr '[' sublist ']' """
    p[0] = ('call', 'exec_bracket', [p[1], p[3]])

def p_expr_5(p):
    """expr : expr LBB sublist ']' ']' """
    p[0] = ('call', 'exec_double_bracket', [p[1], p[3]])

def p_expr_6(p):
    """expr : '{' exprlist '}' """
    p[0] = ('call', 'exec_scope', p[2])

def p_expr_7(p):
    """expr : FUNCTION '(' formlist ')' expr_or_assign_nl %prec LOW """
    p[0] = ('funcion', p[3], p[5])

def p_expr_8(p):
    """expr : SYMBOL '(' sublist ')' """
    p[0] = ('call', p[1], p[3])

## ---------------------------------------------------------------------------------------------------------------------

def p_formlist_1(p):
    """formlist : SYMBOL"""
    p[0] = [('simbolo', p[1])]

def p_formlist_2(p):
    """formlist : SYMBOL EQ_ASSIGN expr"""
    p[0] = [('call', 'exec_assign', [p[1], p[3]])]

def p_formlist_3(p):
    """formlist : formlist ',' SYMBOL"""
    p[0] = p[1]
    p[0].append(('simbolo', p[3]))

def p_formlist_4(p):
    """formlist : formlist ',' SYMBOL EQ_ASSIGN expr"""
    p[0] = p[1]
    p[0].append(('call', 'exec_assign', [p[3], p[5]]))

def p_formlist_empty(p):
    """formlist : empty"""
    p[0] = []

## ---------------------------------------------------------------------------------------------------------------------

def p_sublist_1(p):
    """sublist : sub"""
    p[0] = p[1]

def p_sublist_2(p):
    """sublist : sublist ',' sub"""
    p[0] = p[1]
    p[0].append(p[3])

def p_sub_1(p):
    """sub : empty"""
    p[0] = []

def p_sub_2(p):
    """sub : expr"""
    p[0] = [p[1]]

## ---------------------------------------------------------------------------------------------------------------------

def p_const_or_symbol(p):
    """const_or_symbol : SYMBOL"""
    p[0] = ('simbolo', p[1])

def p_const_or_string(p):
    """const_or_symbol : STR_CONST"""
    p[0] = ('cadena', [p[1]])

def p_const_or_symbol_real(p):
    """const_or_symbol : REAL"""
    p[0] = ('real', [float(p[1])])

def p_const_or_symbol_int(p):
    """const_or_symbol : INT"""
    p[0] = ('entero', [int(p[1])])

def p_const_or_symbol_null(p):
    """const_or_symbol : NULL_CONST"""
    p[0] = ('indefinido', [])

def p_const_or_symbol_true(p):
    """const_or_symbol : TRUE"""
    p[0] = ('logico', [True])

def p_const_or_symbol_false(p):
    """const_or_symbol : FALSE"""
    p[0] = ('logico', [False])

## ---------------------------------------------------------------------------------------------------------------------

def p_binary_operation_plus(p):
    """binary_operation : expr '+' expr"""
    p[0] = ('call', 'exec_sum', [p[1], p[3]])

def p_binary_operation_minus(p):
    """binary_operation : expr '-' expr"""
    p[0] = ('call', 'exec_sub', [p[1], p[3]])

def p_binary_operation_mult(p):
    """binary_operation : expr '*' expr"""
    p[0] = ('call', 'exec_mult', [p[1], p[3]])

def p_binary_operation_pow(p):
    """binary_operation : expr POWER expr"""
    p[0] = ('call', 'exec_pow', [p[1], p[3]])

def p_binary_operation_mod(p):
    """binary_operation : expr MOD expr"""
    p[0] = ('call', 'exec_mod', [p[1], p[3]])

def p_binary_operation_int_div(p):
    """binary_operation : expr INT_DIV expr"""
    p[0] = ('call', 'exec_int_div', [p[1], p[3]])

def p_binary_operation_real_div(p):
    """binary_operation :  expr '/' expr"""
    p[0] = ('call', 'exec_real_div', [p[1], p[3]])

def p_binary_operation_other(p):
    """binary_operation : expr ':' expr
                        | expr '~' expr
                        | expr '?' expr"""
    p[0] = ('call', p[2], [p[1], p[3]])

def p_binary_operation_lt(p):
    """binary_operation : expr LT expr"""
    p[0] = ('call', 'exec_lt', [p[1], p[3]])

def p_binary_operation_le(p):
    """binary_operation : expr LE expr"""
    p[0] = ('call', 'exec_le', [p[1], p[3]])

def p_binary_operation_eq(p):
    """binary_operation : expr EQ expr"""
    p[0] = ('call', 'exec_eq', [p[1], p[3]])

def p_binary_operation_ne(p):
    """binary_operation : expr NE expr"""
    p[0] = ('call', 'exec_ne', [p[1], p[3]])

def p_binary_operation_ge(p):
    """binary_operation : expr GE expr"""
    p[0] = ('call', 'exec_ge', [p[1], p[3]])

def p_binary_operation_gt(p):
    """binary_operation : expr GT expr"""
    p[0] = ('call', 'exec_gt', [p[1], p[3]])

def p_binary_operation_and(p):
    """binary_operation : expr AND expr"""
    p[0] = ('call', 'exec_and', [p[1], p[3]])

def p_binary_operation_or(p):
    """binary_operation : expr OR expr"""
    p[0] = ('call', 'exec_or', [p[1], p[3]])

def p_binary_operation_and2(p):
    """binary_operation : expr AND2 expr """
    p[0] = ('call', 'exec_and2', [p[1], p[3]])

def p_binary_operation_4(p):
    """binary_operation : expr OR2 expr"""
    p[0] = ('call', 'exec_or2', [p[1], p[3]])

def p_binary_operation_matrix(p):
    """binary_operation : expr MATRIX_MULT expr
                        | expr '$' SYMBOL
                        | expr '$' STR_CONST
                        | expr '@' SYMBOL
                        | expr '@' STR_CONST"""
    p[0] = ('call', p[2], [p[1], p[3]])

## ---------------------------------------------------------------------------------------------------------------------

def p_unary_operation_uminus(p):
    """unary_operation :  '-' expr %prec UMINUS"""
    p[0] = ('call', 'exec_uminus', [p[2]])

def p_unary_operation_uplus(p):
    """unary_operation : '+' expr %prec UMINUS"""
    p[0] = ('call', p[1], [p[2]])

def p_unary_operation_other(p):
    """unary_operation :  '!' expr %prec UNOT
                        | '~' expr %prec TILDE
                        | '?' expr"""
    p[0] = ('call', p[1], [p[2]])

## ---------------------------------------------------------------------------------------------------------------------

def p_statement_declaration(p):
    """statement_declaration : if_statement
                             | for_statement
                             | while_statement"""
    p[0] = p[1]

def p_if_statement(p):
    """if_statement : IF '(' expr ')' expr_or_assign_nl else_statement"""
    p[0] = ('call', 'exec_if', [p[3], p[5], p[6]])

def p_else_statement(p):
    """else_statement : empty
                      | ELSE expr_or_assign_nl
                      | NLINE else_statement"""
    p[0] = None if len(p) == 1 else p[2]

def p_for_statement(p):
    """for_statement : FOR '(' SYMBOL IN expr ')' expr_or_assign_nl %prec FOR """
    p[0] = ('call', 'exec_for', [p[3], p[5], p[7]])

def p_while_statement(p):
    """while_statement : WHILE '(' expr ')' expr_or_assign_nl"""
    p[0] = ('call','exec_while', [p[3], p[5]])

## ---------------------------------------------------------------------------------------------------------------------

def p_empty(p):
    """empty : """
    p[0] = None

## ---------------------------------------------------------------------------------------------------------------------

def p_error(p):
    e = "Error de sintaxis "
    if p is not None:
        print (e + "en linea"+ str(p.lexer.lineno) + " -> Token no esperado '" + str(p.value) + "'")
    else:
        print (e)


def buscarFicheros(directorio):
    ficheros = []
    numArchivo = ''
    respuesta = False
    cont = 1

    for base, dirs, files in os.walk(directorio):
        ficheros.append(files)

    for file in files:
        print(str(cont)+". "+str(file))
        cont = cont+1

    while respuesta== False:
        numArchivo = input('\nNumero del test: ')
        for file in files:
            if file == files[int(numArchivo)-1]:
                respuesta = True
                break

    print('Has escogido \"%s\"\n' %(files[int(numArchivo)-1]))
    
    return files[int(numArchivo)-1]



directorio = 'C:/Users/Andrey/Documents/Git/Compiladores/InterpreteR/Tests/'
archivo = buscarFicheros(directorio)
test = directorio+archivo
fp = codecs.open(test,"r","utf-8")
cadena = fp.read()
fp.close()  


parser = yacc.yacc()
result = parser.parse(cadena)


print(result)