# An implementation of Dartmouth BASIC (1964)
#

from ply import *
import basiclex

tokens = basiclex.tokens

precedence = (
    ('left', 'PLUS','PLUSL','PLUSR','MINUS','MINUSR','MINUSL'),
    ('left', 'TIMES','TIMESR','TIMESL', 'DIVIDE','DIVIDEL','DIVIDER'),
    ('left', 'POWER','POWERL','POWERR'),
    ('right', 'UMINUS')
)

# A BASIC program is a series of statements.  We represent the program as a
# dictionary of tuples indexed by line number.


def p_program(p):
    '''program : program statement
               | statement'''
    if len(p) == 2 and p[1]:
        p.counter = 0
        p[0] = {}
        p[0][p.counter] = p[1]
        p.counter += 1
        # print(p[0])
    elif len(p) == 3:
        p[0] = p[1]
        if not p[0]:
            p[0] = {}
        if p[2]:
            stat = p[2]
            p[0][p.counter] = stat
            p.counter += 1
        # print(p[0])

# This catch-all rule is used for any catastrophic errors.  In this case,
# we simply return nothing


def p_program_error(p):
    '''program : error'''
    p[0] = None
    p.parser.error = 1
    print("PROGRAM ERROR")

# Format of all BASIC statements.


def p_statement(p):
    '''statement : command NEWLINE
                 | command statement'''
    if isinstance(p[1], str):
        print("%s %s %s" % (p[1], "AT1 LINE", p[1]))
        p[0] = None
        p.parser.error = 1
    else:
        
        p[0] = p[1]



def p_statement_blank(p):
    '''statement : INTEGER NEWLINE'''
    p[0] = (0, ('BLANK', int(p[1])))



# Error handling for malformed statements


def p_statement_bad(p):
    '''statement : INTEGER error NEWLINE'''
    print("MALFORMED STATEMENT AT LINE %s" % p[1])
    p[0] = None
    p.parser.error = 1

# Blank line


def p_statement_newline(p):
    '''statement : NEWLINE'''
    p[0] = None

# VARIABLE statement


def p_command_num(p):
    '''command : NUMERIC variable'''
    p[0] = ('NUMERIC', p[2])


def p_command_bool(p):
    '''command : LOGIC variable'''
    p[0] = ('LOGIC', p[2])
	

def p_command_str(p):
    '''command : STRING variable'''
    p[0] = ('STRING', p[2])	

def p_command_assign(p):
    '''command : variable EQUALS expr'''
    p[0] = ('ASSIGN', p[1], p[3])
	
def p_command_assignt(p):
    '''command : variable EQUALS TRUE'''
    p[0] = ('ASSIGN', p[1], p[3])
	
def p_command_assigntf(p):
    '''command : variable EQUALS FALSE'''
    p[0] = ('ASSIGN', p[1], p[3])
	
def p_command_bad(p):
    '''command : variable EQUALS error'''
    p[0] = "BAD EXPRESSION"

# DATA statement


def p_command_rec(p):
    '''command : RECORD variable DATA LPAREN variablegroup RPAREN'''
    p[0] = ('RECORD', p[2], p[5])

def p_command_rec_to(p):
    '''command : RECORD variable DATA CONVERSION TO variablegroup'''
    p[0] = ('RECORD', 'TO', p[2], p[6])

def p_command_rec_from(p):
    '''command : RECORD variable DATA CONVERSION FROM variablegroup'''
    p[0] = ('RECORD', 'FROM', p[2], p[6])


def p_variablegroup(p):
    '''variablegroup : variablegroup COMMA command
                     | command'''
    if len(p) == 4:
        p[0] = p[1]
        p[0].append(p[3])
    else:
        p[0] = [p[1]]



# PRINT statement


def p_command_print(p):
    '''command : PRINT plist optend'''
    p[0] = ('PRINT', p[2], p[3])


def p_command_print_bad(p):
    '''command : PRINT error'''
    p[0] = "MALFORMED PRINT STATEMENT"

# Optional ending on PRINT. Either a comma (,) or semicolon (;)


def p_optend(p):
    '''optend : COMMA 
              | SEMI
              |'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = None

# PRINT statement with no arguments


def p_command_print_empty(p):
    '''command : PRINT'''
    p[0] = ('PRINT', [], None)


def p_command_if(p):
    '''command : LCURL relexpr RCURL BLOCK statgroup UNBLOCK'''
    p[0] = ('WHILE', p[2], p[5])

def p_command_func(p):
    'command : PROC variable LCURL variables RCURL BLOCK statgroup UNBLOCK'
    p[0] = ('PROC', p[2], p[4], p[7])


def p_variables(p):
    '''variables : variables COMMA command
                 | variables COMMA command MOD
                 | command MOD
                 | command'''
    if len(p) == 4:
        p[0] = p[1]
        p[0].append(p[3])
    elif len(p) == 5:
        p[0] = p[1]
        p[0].append(p[3])
        p[0].append(p[4])
    elif len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = (p[1],p[2])

def p_dimlist(p):
    '''dimlist : dimlist COMMA dimitem
               | dimitem'''
    if len(p) == 4:
        p[0] = p[1]
        p[0].append(p[3])
    else:
        p[0] = [p[1]]

def p_statgroup(p):
    'statgroup : statement'
    p[0] = ('STATGROUP', p[1])

def p_statgroup_cont(p):
    '''statgroup : statgroup statement
                 | statgroup command'''
    p[0] = ('STATGROUP', p[1], p[2])


def p_command_end(p):
    '''command : END'''
    p[0] = ('END',)

# DIM statement


def p_command_dim(p):
    '''command : DIM dimlist'''
    p[0] = ('DIM', p[2])


def p_command_dim_bad(p):
    '''command : DIM error'''
    p[0] = "MALFORMED VARIABLE LIST IN DIM"

# List of variables supplied to DIM statement


def p_dimlist(p):
    '''dimlist : dimlist COMMA dimitem
               | dimitem'''
    if len(p) == 4:
        p[0] = p[1]
        p[0].append(p[3])
    else:
        p[0] = [p[1]]

# DIM items


def p_dimitem_single(p):
    '''dimitem : ID LPAREN INTEGER RPAREN'''
    p[0] = (p[1], eval(p[3]), 0)


def p_dimitem_double(p):
    '''dimitem : ID LPAREN INTEGER COMMA INTEGER RPAREN'''
    p[0] = (p[1], eval(p[3]), eval(p[5]))

# Arithmetic expressions


def p_expr_binary(p):
    '''expr : expr PLUS expr
            | expr PLUSR expr
			| expr PLUSL expr
			| expr MINUS expr
			| expr MINUSR expr
			| expr MINUSL expr
            | expr TIMES expr
            | expr TIMESL expr
            | expr TIMESR expr
            | expr DIVIDE expr
            | expr DIVIDEL expr
            | expr DIVIDER expr
            | expr POWER expr
            | expr POWERL expr
            | expr POWERR expr'''

    p[0] = ('BINOP', p[2], p[1], p[3])


def p_expr_number(p):
    '''expr : INTEGER'''
    p[0] = ('NUM', eval(p[1]))


def p_expr_variable(p):
    '''expr : variable'''
    p[0] = ('VAR', p[1])


def p_expr_group(p):
    '''expr : LPAREN expr RPAREN'''
    p[0] = ('GROUP', p[2])


def p_expr_unary(p):
    '''expr : MINUS expr %prec UMINUS'''
    p[0] = ('UNARY', '-', p[2])

# Relational expressions


def p_relexpr(p):
    '''relexpr : expr LT expr
               | expr GT expr
               | expr GE expr
               | expr NE expr
               | expr LTL expr
               | expr GTL expr
               | expr GEL expr
               | expr NEL expr
               | expr LTR expr
               | expr GTR expr
               | expr GER expr
               | expr NER expr'''
    p[0] = ('RELOP', p[2], p[1], p[3])

# Variables


def p_variable(p):
    '''variable : ID
              | ID LPAREN expr RPAREN
              | ID LPAREN expr COMMA expr RPAREN'''
    if len(p) == 2:
        p[0] = (p[1], None, None)
    elif len(p) == 5:
        p[0] = (p[1], p[3], None)
    else:
        p[0] = (p[1], p[3], p[5])

# Builds a list of variable targets as a Python list


def p_varlist(p):
    '''varlist : varlist COMMA variable
               | variable'''
    if len(p) > 2:
        p[0] = p[1]
        p[0].append(p[3])
    else:
        p[0] = [p[1]]


# Builds a list of numbers as a Python list

def p_numlist(p):
    '''numlist : numlist COMMA number
               | number'''

    if len(p) > 2:
        p[0] = p[1]
        p[0].append(p[3])
    else:
        p[0] = [p[1]]

# A number. May be an integer or a float


def p_number(p):
    'number  : INTEGER'
    p[0] = eval(p[1])

# A signed number.


def p_number_signed(p):
    'number  : MINUS INTEGER'
    p[0] = eval("-" + p[2])

# List of targets for a print statement
# Returns a list of tuples (label,expr)


def p_plist(p):
    '''plist   : plist COMMA pitem
               | pitem'''
    if len(p) > 3:
        p[0] = p[1]
        p[0].append(p[3])
    else:
        p[0] = [p[1]]


def p_item_string(p):
    '''pitem : STRING'''
    p[0] = (p[1][1:-1], None)


def p_item_string_expr(p):
    '''pitem : STRING expr'''
    p[0] = (p[1][1:-1], p[2])


def p_item_expr(p):
    '''pitem : expr'''
    p[0] = ("", p[1])

# Catastrophic error handler


def p_error(p):
    if not p:
        print("SYNTAX ERROR AT EOF")

bparser = yacc.yacc()


def parse(data, debug=0):
    bparser.error = 0
    p = bparser.parse(data, debug=debug)
    if bparser.error:
        return None
    return p
