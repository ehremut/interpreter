# An implementation of Dartmouth BASIC (1964)
#

import sys
import basiclex
import basparse
import basinterp

data = open('program').read()
prog = basparse.parse(data)
if not prog:
    raise SystemExit
b = basinterp.BasicInterpreter(prog)
try:
	b.run()
	print(b.vars)
	#print(b.lists)
	#print(b.tables)


except RuntimeError:
    pass
