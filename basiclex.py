# An implementation of Dartmouth BASIC (1964)

from ply import *

keywords = (
    'NUMERIC', 'LOGIC', 'TRUE', 'FALSE', 'DIM', 'STRING', 'DATA','BLOCK','UNBLOCK','PRINT', 'TO', 'END', 'RECORD', 'CONVERSION',
    'FROM', 'PROC', 'FUNC', 'STOP'
)

tokens = keywords + (
    'EQUALS', 'PLUS','PLUSR','PLUSL', 'MINUS','MINUSR','MINUSL','TIMES','TIMESL', 'TIMESR', 'DIVIDE','DIVIDEL','DIVIDER', 'POWER','POWERL','POWERR',
    'LPAREN', 'RPAREN','LCURL', 'RCURL','LT', 'GT', 'GE', 'NE','LTL', 'GTL', 'GEL', 'NEL','LTR', 'GTR', 'GER', 'NER',
    'COMMA', 'SEMI', 'INTEGER', 'FLOAT', 'MOD',
    'ID', 'NEWLINE'
)

t_ignore = ' \t'



def t_ID(t):
    r'[A-Z][A-Z0-9]*'
    if t.value in keywords:
        t.type = t.value
    return t

t_MOD = r'&'
t_EQUALS = r'='
t_PLUS = r'\+'
t_PLUSR = r'\+\.'
t_PLUSL = r'\.\+'
t_MINUS = r'\-'
t_MINUSR = r'\-\.'
t_MINUSL = r'\.\-'
t_TIMES = r'\*'
t_TIMESL = r'\.\*'
t_TIMESR = r'\*\.'
t_POWER = r'\^'
t_POWERL = r'\.\^'
t_POWERR = r'\^\.'
t_DIVIDE = r'/'
t_DIVIDEL = r'./'
t_DIVIDER = r'/.'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LTL = r'\.<'
t_GTL = r'\.>'
t_NEL = r'\.!'
t_GEL = r'\.\?'
t_LTR = r'<\.'
t_GTR = r'>\.'
t_NER = r'!\.'
t_GER = r'\?\.'
t_LT = r'<'
t_GT = r'>'
t_NE = r'!'
t_GE = r'\?'
t_LCURL = r'\{'
t_RCURL = r'\}'
t_COMMA = r'\,'
t_SEMI = r';'
t_INTEGER = r'\d+'
t_FLOAT = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
t_STRING = r'\".*?\"'


def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    return t


def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)

lex.lex(debug=0)
