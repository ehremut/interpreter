# This file provides the runtime support for running a basic program
# Assumes the program has been parsed using basparse.py

import sys
import math
import random


class BasicInterpreter:

    # Initialize the interpreter. prog is a dictionary
    # containing (line,statement) mappings
    def __init__(self, prog):
        self.prog = prog



    # Collect all data statements
    def collect_data(self):
        self.data = []
        for lineno in self.stat:
            if self.prog[lineno][0] == 'DATA':
                self.data = self.data + self.prog[lineno][1]
        self.dc = 0                  # Initialize the data counter

    # Check for end statements
    def check_end(self):
        has_end = 0
        for lineno in self.stat:
            if self.prog[lineno][0] == 'END' and not has_end:
                has_end = lineno
        if not has_end:
            print("NO END INSTRUCTION")
            self.error = 1
            return
        if has_end != lineno:
            print("END IS NOT LAST")
            self.error = 1

    # Check loops

    # Evaluate an expression
    def eval(self, expr):
        if expr=='UNDEF':
            return 'UNDEF'
        if expr=='TRUE':
            return 'TRUE'
        if expr=='FALSE':
            return 'FALSE'
        etype = expr[0]
        if etype == 'NUM':
            return expr[1]
        elif etype == 'GROUP':
            return self.eval(expr[1])
        elif etype == 'UNARY':
            if expr[1] == '-':
                eval1 = self.eval(expr[2])
                if (type(eval1) is int):
                    s=[]
                    s.append(-eval1)
                    s.append('NUMERIC')
                    return s
                elif eval1[1]=='NUMERIC':
                    if eval1[0]=='UNDEF':
                        return eval1
                    else :
                        s=[]
                        s.append(-eval1[0])
                        s.append('NUMERIC')
                        return s
                elif eval1[1]=='LOGIC':
                    if eval1[0]=='UNDEF':
                        s=[]
                        s.append('UNDEF')
                        s.append('LOGIC')
                        return s
                    elif eval1[0]=='TRUE' :
                        s=[]
                        s.append('FALSE')
                        s.append('LOGIC')
                        return s
                    elif eval1[0]=='FALSE' :
                        s=[]
                        s.append('TRUE')
                        s.append('LOGIC')
                        return s
                
        elif etype == 'BINOP':
            if expr[1] == '+':
                eval1 = self.eval(expr[2])
                eval2 = self.eval(expr[3])
                
                b=[]
                if (type(eval1) is int or eval1[1]=='NUMERIC') and (type(eval2) is int or eval2[1]=='NUMERIC'):
                    if type(eval2) is int and type(eval1) is int:
                        b.append(eval1+eval2)
                    elif type(eval2) is int and not type(eval1) is int:
                        if eval1[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval1[0]+eval2)
                    
                    elif not type(eval2) is int and type(eval1) is int:
                        if eval2[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval2[0]+eval1)
                    elif not type(eval2) is int and not type(eval1) is int:
                        if eval1[0]=='UNDEF' or eval2[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval1[0]+eval2[0])
                    b.append('NUMERIC')
                    return b
                if (eval1[1]=='LOGIC') and (eval2[1]=='LOGIC'):
                    
                    if (eval1[0]=='FALSE') and (eval2[0]=='FALSE'):
                        b.append('FALSE')
                    if (eval1[0]=='FALSE') and (eval2[0]=='TRUE'):
                        b.append('TRUE')
                    if (eval1[0]=='TRUE') and (eval2[0]=='FALSE'):
                        b.append('TRUE')
                    if (eval1[0]=='TRUE') and (eval2[0]=='TRUE'):
                        b.append('TRUE')
                    if (eval1[0]=='FALSE') and (eval2[0]=='UNDEF'):
                        b.append('UNDEF')
                    if (eval1[0]=='UNDEF') and (eval2[0]=='FALSE'):
                        b.append('UNDEF')
                    if (eval1[0]=='TRUE') and (eval2[0]=='UNDEF'):
                        b.append('TRUE')
                    if (eval1[0]=='UNDEF') and (eval2[0]=='TRUE'):
                        b.append('TRUE')
                    if (eval1[0]=='UNDEF') and (eval2[0]=='UNDEF'):
                        b.append('UNDEF')
                    b.append('LOGIC')
                    
                    return b
            elif expr[1] == '+.':
                eval1 = self.eval(expr[2])
                eval2 = self.eval(expr[3])
               
                b=[]
                if (type(eval1) is int or eval1[1]=='NUMERIC') and (eval2[1]=='LOGIC'):
                    if (eval2[0]=='TRUE'):
                        eval2=1
                    elif (eval2[0]=='FALSE'):
                        eval2=0
                    if type(eval2) is int and type(eval1) is int:
                        b.append(eval1+eval2)
                    elif type(eval2) is int and not type(eval1) is int:
                        if eval1[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval1[0]+eval2)
                    
                    elif not type(eval2) is int and type(eval1) is int:
                        if eval2[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval2[0]+eval1)
                    elif not type(eval2) is int and not type(eval1) is int:
                        if eval1[0]=='UNDEF' or eval2[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval1[0]+eval2[0])
                    b.append('NUMERIC')
                    return b
                if (eval1[1]=='LOGIC') and (type(eval2) is int or eval2[1]=='NUMERIC') :
                    if(type(eval2) is int):
                        
                        if(eval2>=0):
                            eva2=[]
                            eva2.append('TRUE')
                        else:
                            eva2=[]
                            eva2.append('FALSE')
                    else:
                        if ((eval2[0])=='UNDEF'):
                            eva2=[]
                            eva2.append('UNDEF')
                        elif ((eval2[0])>=0):
                            eva2=[]
                            eva2.append('TRUE')
                        elif ((eval2[0])<0):
                            eva2=[]
                            eva2.append('FALSE')
                        
                    
                    if (eval1[0]=='FALSE') and (eva2[0]=='FALSE'):
                        b.append('FALSE')
                    if (eval1[0]=='FALSE') and (eva2[0]=='TRUE'):
                        b.append('TRUE')
                    if (eval1[0]=='TRUE') and (eva2[0]=='FALSE'):
                        b.append('TRUE')
                    if (eval1[0]=='TRUE') and (eva2[0]=='TRUE'):
                        b.append('TRUE')
                    if (eval1[0]=='FALSE') and (eva2[0]=='UNDEF'):
                        b.append('UNDEF')
                    if (eval1[0]=='UNDEF') and (eva2[0]=='FALSE'):
                        b.append('UNDEF')
                    if (eval1[0]=='TRUE') and (eva2[0]=='UNDEF'):
                        b.append('TRUE')
                    if (eval1[0]=='UNDEF') and (eva2[0]=='TRUE'):
                        b.append('TRUE')
                    if (eval1[0]=='UNDEF') and (eva2[0]=='UNDEF'):
                        b.append('UNDEF')
                    b.append('LOGIC')
                    
                    return b

            elif expr[1] == '.+':
                eval1 = self.eval(expr[2])
                eval2 = self.eval(expr[3])
               
                b=[]
                if (type(eval2) is int or eval2[1]=='NUMERIC') and (eval1[1]=='LOGIC'):
                    if (eval1[0]=='TRUE'):
                        eval1=1
                    elif (eval1[0]=='FALSE'):
                        eval1=0
                    if type(eval2) is int and type(eval1) is int:
                        b.append(eval1+eval2)
                    elif type(eval2) is int and not type(eval1) is int:
                        if eval1[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval1[0]+eval2)
                    
                    elif not type(eval2) is int and type(eval1) is int:
                        if eval2[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval2[0]+eval1)
                    elif not type(eval2) is int and not type(eval1) is int:
                        if eval1[0]=='UNDEF' or eval2[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval1[0]+eval2[0])
                    b.append('NUMERIC')
                    return b
                if (eval2[1]=='LOGIC') and (type(eval1) is int or eval1[1]=='NUMERIC') :
                    if(type(eval1) is int):
                        
                        if(eval1>=0):
                            eva1=[]
                            eva1.append('TRUE')
                        else:
                            eva1=[]
                            eva1.append('FALSE')
                    else:
                        if ((eval1[0])=='UNDEF'):
                            eva1=[]
                            eva1.append('UNDEF')
                        elif ((eval1[0])>=0):
                            eva1=[]
                            eva1.append('TRUE')
                        elif ((eval1[0])<0):
                            eva1=[]
                            eva1.append('FALSE')
                        
                    
                    if (eva1[0]=='FALSE') and (eval2[0]=='FALSE'):
                        b.append('FALSE')
                    if (eva1[0]=='FALSE') and (eval2[0]=='TRUE'):
                        b.append('TRUE')
                    if (eva1[0]=='TRUE') and (eval2[0]=='FALSE'):
                        b.append('TRUE')
                    if (eva1[0]=='TRUE') and (eval2[0]=='TRUE'):
                        b.append('TRUE')
                    if (eva1[0]=='FALSE') and (eval2[0]=='UNDEF'):
                        b.append('UNDEF')
                    if (eva1[0]=='UNDEF') and (eval2[0]=='FALSE'):
                        b.append('UNDEF')
                    if (eva1[0]=='TRUE') and (eval2[0]=='UNDEF'):
                        b.append('TRUE')
                    if (eva1[0]=='UNDEF') and (eval2[0]=='TRUE'):
                        b.append('TRUE')
                    if (eva1[0]=='UNDEF') and (eval2[0]=='UNDEF'):
                        b.append('UNDEF')
                    b.append('LOGIC')
                    
                    return b


            elif expr[1] == '-':
                eval1 = self.eval(expr[2])
                eval2 = self.eval(expr[3])
                b=[]
                if (type(eval1) is int or eval1[1]=='NUMERIC') and (type(eval2) is int or eval2[1]=='NUMERIC'):
                    if type(eval2) is int and type(eval1) is int:
                        b.append(eval1-eval2)
                    elif type(eval2) is int and not type(eval1) is int:
                        if eval1[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval1[0]-eval2)
                    
                    elif not type(eval2) is int and type(eval1) is int:
                        if eval2[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval1-eval2[0])
                    elif not type(eval2) is int and not type(eval1) is int:
                        if eval1[0]=='UNDEF' or eval2[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval1[0]-eval2[0])
                    b.append('NUMERIC')
                    return b
                if (eval1[1]=='LOGIC') and (eval2[1]=='LOGIC'):
                    
                    if (eval1[0]=='FALSE') and (eval2[0]=='FALSE'):
                        b.append('FALSE')
                    if (eval1[0]=='FALSE') and (eval2[0]=='TRUE'):
                        b.append('TRUE')
                    if (eval1[0]=='TRUE') and (eval2[0]=='FALSE'):
                        b.append('TRUE')
                    if (eval1[0]=='TRUE') and (eval2[0]=='TRUE'):
                        b.append('FALSE')
                    if (eval1[0]=='FALSE') and (eval2[0]=='UNDEF'):
                        b.append('UNDEF')
                    if (eval1[0]=='UNDEF') and (eval2[0]=='FALSE'):
                        b.append('UNDEF')
                    if (eval1[0]=='TRUE') and (eval2[0]=='UNDEF'):
                        b.append('UNDEF')
                    if (eval1[0]=='UNDEF') and (eval2[0]=='TRUE'):
                        b.append('UNDEF')
                    if (eval1[0]=='UNDEF') and (eval2[0]=='UNDEF'):
                        b.append('UNDEF')
                    b.append('LOGIC')
                    return b
                
            elif expr[1] == '-.':
                eval1 = self.eval(expr[2])
                eval2 = self.eval(expr[3])
               
                b=[]
                if (type(eval1) is int or eval1[1]=='NUMERIC') and (eval2[1]=='LOGIC'):
                    if (eval2[0]=='TRUE'):
                        eval2=1
                    elif (eval2[0]=='FALSE'):
                        eval2=0
                    if type(eval2) is int and type(eval1) is int:
                        b.append(eval1-eval2)
                    elif type(eval2) is int and not type(eval1) is int:
                        if eval1[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval1[0]-eval2)
                    
                    elif not type(eval2) is int and type(eval1) is int:
                        if eval2[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval1-eval2[0])
                    elif not type(eval2) is int and not type(eval1) is int:
                        if eval1[0]=='UNDEF' or eval2[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval1[0]-eval2[0])
                    b.append('NUMERIC')
                    return b
                if (eval1[1]=='LOGIC') and (type(eval2) is int or eval2[1]=='NUMERIC') :
                    if(type(eval2) is int):
                        
                        if(eval2>=0):
                            eva2=[]
                            eva2.append('TRUE')
                        else:
                            eva2=[]
                            eva2.append('FALSE')
                    else:
                        if ((eval2[0])=='UNDEF'):
                            eva2=[]
                            eva2.append('UNDEF')
                        elif ((eval2[0])>=0):
                            eva2=[]
                            eva2.append('TRUE')
                        elif ((eval2[0])<0):
                            eva2=[]
                            eva2.append('FALSE')
                        
                    
                    if (eval1[0]=='FALSE') and (eva2[0]=='FALSE'):
                        b.append('FALSE')
                    if (eval1[0]=='FALSE') and (eva2[0]=='TRUE'):
                        b.append('TRUE')
                    if (eval1[0]=='TRUE') and (eva2[0]=='FALSE'):
                        b.append('TRUE')
                    if (eval1[0]=='TRUE') and (eva2[0]=='TRUE'):
                        b.append('FALSE')
                    if (eval1[0]=='FALSE') and (eva2[0]=='UNDEF'):
                        b.append('UNDEF')
                    if (eval1[0]=='UNDEF') and (eva2[0]=='FALSE'):
                        b.append('UNDEF')
                    if (eval1[0]=='TRUE') and (eva2[0]=='UNDEF'):
                        b.append('UNDEF')
                    if (eval1[0]=='UNDEF') and (eva2[0]=='TRUE'):
                        b.append('UNDEF')
                    if (eval1[0]=='UNDEF') and (eva2[0]=='UNDEF'):
                        b.append('UNDEF')
                    b.append('LOGIC')
                    
                    return b

            elif expr[1] == '.-':
                eval1 = self.eval(expr[2])
                eval2 = self.eval(expr[3])
               
                b=[]
                if (type(eval2) is int or eval2[1]=='NUMERIC') and (eval1[1]=='LOGIC'):
                    if (eval1[0]=='TRUE'):
                        eval1=1
                    elif (eval1[0]=='FALSE'):
                        eval1=0
                    if type(eval2) is int and type(eval1) is int:
                        b.append(eval1-eval2)
                    elif type(eval2) is int and not type(eval1) is int:
                        if eval1[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval1[0]-eval2)
                    
                    elif not type(eval2) is int and type(eval1) is int:
                        if eval2[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval1-eval2[0])
                    elif not type(eval2) is int and not type(eval1) is int:
                        if eval1[0]=='UNDEF' or eval2[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval1[0]-eval2[0])
                    b.append('NUMERIC')
                    return b
                if (eval2[1]=='LOGIC') and (type(eval1) is int or eval1[1]=='NUMERIC') :
                    if(type(eval1) is int):
                        
                        if(eval1>=0):
                            eva1=[]
                            eva1.append('TRUE')
                        else:
                            eva1=[]
                            eva1.append('FALSE')
                    else:
                        if ((eval1[0])=='UNDEF'):
                            eva1=[]
                            eva1.append('UNDEF')
                        elif ((eval1[0])>=0):
                            eva1=[]
                            eva1.append('TRUE')
                        elif ((eval1[0])<0):
                            eva1=[]
                            eva1.append('FALSE')
                        
                    
                    if (eva1[0]=='FALSE') and (eval2[0]=='FALSE'):
                        b.append('FALSE')
                    if (eva1[0]=='FALSE') and (eval2[0]=='TRUE'):
                        b.append('TRUE')
                    if (eva1[0]=='TRUE') and (eval2[0]=='FALSE'):
                        b.append('TRUE')
                    if (eva1[0]=='TRUE') and (eval2[0]=='TRUE'):
                        b.append('FALSE')
                    if (eva1[0]=='FALSE') and (eval2[0]=='UNDEF'):
                        b.append('UNDEF')
                    if (eva1[0]=='UNDEF') and (eval2[0]=='FALSE'):
                        b.append('UNDEF')
                    if (eva1[0]=='TRUE') and (eval2[0]=='UNDEF'):
                        b.append('UNDEF')
                    if (eva1[0]=='UNDEF') and (eval2[0]=='TRUE'):
                        b.append('UNDEF')
                    if (eva1[0]=='UNDEF') and (eval2[0]=='UNDEF'):
                        b.append('UNDEF')
                    b.append('LOGIC')
                    
                    return b
                
            elif expr[1] == '*':
                eval1 = self.eval(expr[2])
                eval2 = self.eval(expr[3])
                b=[]
                if (type(eval1) is int or eval1[1]=='NUMERIC') and (type(eval2) is int or eval2[1]=='NUMERIC'):
                    if type(eval2) is int and type(eval1) is int:
                        b.append(eval1*eval2)
                    elif type(eval2) is int and not type(eval1) is int:
                        if eval1[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval1[0]*eval2)
                    
                    elif not type(eval2) is int and type(eval1) is int:
                        if eval2[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval2[0]*eval1)
                    elif not type(eval2) is int and not type(eval1) is int:
                        if eval1[0]=='UNDEF' or eval2[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval1[0]*eval2[0])
                    b.append('NUMERIC')
                    return b
                if (eval1[1]=='LOGIC') and (eval2[1]=='LOGIC'):
                    
                    if (eval1[0]=='FALSE') and (eval2[0]=='FALSE'):
                        b.append('FALSE')
                    if (eval1[0]=='FALSE') and (eval2[0]=='TRUE'):
                        b.append('FALSE')
                    if (eval1[0]=='TRUE') and (eval2[0]=='FALSE'):
                        b.append('FALSE')
                    if (eval1[0]=='TRUE') and (eval2[0]=='TRUE'):
                        b.append('TRUE')
                    if (eval1[0]=='FALSE') and (eval2[0]=='UNDEF'):
                        b.append('FALSE')
                    if (eval1[0]=='UNDEF') and (eval2[0]=='FALSE'):
                        b.append('FALSE')
                    if (eval1[0]=='TRUE') and (eval2[0]=='UNDEF'):
                        b.append('UNDEF')
                    if (eval1[0]=='UNDEF') and (eval2[0]=='TRUE'):
                        b.append('UNDEF')
                    if (eval1[0]=='UNDEF') and (eval2[0]=='UNDEF'):
                        b.append('UNDEF')
                    b.append('LOGIC')
                    return b

            elif expr[1] == '*.':
                eval1 = self.eval(expr[2])
                eval2 = self.eval(expr[3])
               
                b=[]
                if (type(eval1) is int or eval1[1]=='NUMERIC') and (eval2[1]=='LOGIC'):
                    if (eval2[0]=='TRUE'):
                        eval2=1
                    elif (eval2[0]=='FALSE'):
                        eval2=0
                    if type(eval2) is int and type(eval1) is int:
                        b.append(eval1*eval2)
                    elif type(eval2) is int and not type(eval1) is int:
                        if eval1[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval1[0]*eval2)
                    
                    elif not type(eval2) is int and type(eval1) is int:
                        if eval2[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval2[0]*eval1)
                    elif not type(eval2) is int and not type(eval1) is int:
                        if eval1[0]=='UNDEF' or eval2[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval1[0]*eval2[0])
                    b.append('NUMERIC')
                    return b
                if (eval1[1]=='LOGIC') and (type(eval2) is int or eval2[1]=='NUMERIC') :
                    if(type(eval2) is int):
                        
                        if(eval2>=0):
                            eva2=[]
                            eva2.append('TRUE')
                        else:
                            eva2=[]
                            eva2.append('FALSE')
                    else:
                        
                        
                        if ((eval2[0])=='UNDEF'):
                            eva2=[]
                            eva2.append('UNDEF')
                        elif ((eval2[0])>=0):
                            eva2=[]
                            eva2.append('TRUE')
                        elif ((eval2[0])<0):
                            eva2=[]
                            eva2.append('FALSE')
                        
                    
                    if (eval1[0]=='FALSE') and (eva2[0]=='FALSE'):
                        b.append('FALSE')
                    if (eval1[0]=='FALSE') and (eva2[0]=='TRUE'):
                        b.append('FALSE')
                    if (eval1[0]=='TRUE') and (eva2[0]=='FALSE'):
                        b.append('FALSE')
                    if (eval1[0]=='TRUE') and (eva2[0]=='TRUE'):
                        b.append('TRUE')
                    if (eval1[0]=='FALSE') and (eva2[0]=='UNDEF'):
                        b.append('FALSE')
                    if (eval1[0]=='UNDEF') and (eva2[0]=='FALSE'):
                        b.append('FALSE')
                    if (eval1[0]=='TRUE') and (eva2[0]=='UNDEF'):
                        b.append('UNDEF')
                    if (eval1[0]=='UNDEF') and (eva2[0]=='TRUE'):
                        b.append('UNDEF')
                    if (eval1[0]=='UNDEF') and (eva2[0]=='UNDEF'):
                        b.append('UNDEF')
                    b.append('LOGIC')
                    
                    return b

            elif expr[1] == '.*':
                eval1 = self.eval(expr[2])
                eval2 = self.eval(expr[3])
               
                b=[]
                if (type(eval2) is int or eval2[1]=='NUMERIC') and (eval1[1]=='LOGIC'):
                    if (eval1[0]=='TRUE'):
                        eval1=1
                    elif (eval1[0]=='FALSE'):
                        eval1=0
                    if type(eval2) is int and type(eval1) is int:
                        b.append(eval1*eval2)
                    elif type(eval2) is int and not type(eval1) is int:
                        if eval1[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval1[0]*eval2)
                    
                    elif not type(eval2) is int and type(eval1) is int:
                        if eval2[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval2[0]*eval1)
                    elif not type(eval2) is int and not type(eval1) is int:
                        if eval1[0]=='UNDEF' or eval2[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval1[0]*eval2[0])
                    b.append('NUMERIC')
                    return b
                if (eval2[1]=='LOGIC') and (type(eval1) is int or eval1[1]=='NUMERIC') :
                    if(type(eval1) is int):
                        
                        if(eval1>=0):
                            eva1=[]
                            eva1.append('TRUE')
                        else:
                            eva1=[]
                            eva1.append('FALSE')
                    else:
                        if ((eval1[0])=='UNDEF'):
                            eva1=[]
                            eva1.append('UNDEF')
                        elif ((eval1[0])>=0):
                            eva1=[]
                            eva1.append('TRUE')
                        elif ((eval1[0])<0):
                            eva1=[]
                            eva1.append('FALSE')
                        
                    
                    if (eva1[0]=='FALSE') and (eval2[0]=='FALSE'):
                        b.append('FALSE')
                    if (eva1[0]=='FALSE') and (eval2[0]=='TRUE'):
                        b.append('FALSE')
                    if (eva1[0]=='TRUE') and (eval2[0]=='FALSE'):
                        b.append('FALSE')
                    if (eva1[0]=='TRUE') and (eval2[0]=='TRUE'):
                        b.append('TRUE')
                    if (eva1[0]=='FALSE') and (eval2[0]=='UNDEF'):
                        b.append('FALSE')
                    if (eva1[0]=='UNDEF') and (eval2[0]=='FALSE'):
                        b.append('FALSE')
                    if (eva1[0]=='TRUE') and (eval2[0]=='UNDEF'):
                        b.append('UNDEF')
                    if (eva1[0]=='UNDEF') and (eval2[0]=='TRUE'):
                        b.append('UNDEF')
                    if (eva1[0]=='UNDEF') and (eval2[0]=='UNDEF'):
                        b.append('UNDEF')
                    b.append('LOGIC')
                    
                    return b


                            
            elif expr[1] == '/':
                eval1 = self.eval(expr[2])
                eval2 = self.eval(expr[3])
                b=[]
                if (type(eval1) is int or eval1[1]=='NUMERIC') and (type(eval2) is int or eval2[1]=='NUMERIC'):
                    if type(eval2) is int and type(eval1) is int:
                        b.append(eval1/eval2)
                    elif type(eval2) is int and not type(eval1) is int:
                        if eval1[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval1[0]/eval2)
                    
                    elif not type(eval2) is int and type(eval1) is int:
                        if eval2[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval2[0]/eval1)
                    elif not type(eval2) is int and not type(eval1) is int:
                        if eval1[0]=='UNDEF' or eval2[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval1[0]/eval2[0])
                    b.append('NUMERIC')
                    return b
                if (eval1[1]=='LOGIC') and (eval2[1]=='LOGIC'):
                    
                    if (eval1[0]=='FALSE') and (eval2[0]=='FALSE'):
                        b.append('TRUE')
                    if (eval1[0]=='FALSE') and (eval2[0]=='TRUE'):
                        b.append('TRUE')
                    if (eval1[0]=='TRUE') and (eval2[0]=='FALSE'):
                        b.append('TRUE')
                    if (eval1[0]=='TRUE') and (eval2[0]=='TRUE'):
                        b.append('FALSE')
                    if (eval1[0]=='FALSE') and (eval2[0]=='UNDEF'):
                        b.append('TRUE')
                    if (eval1[0]=='UNDEF') and (eval2[0]=='FALSE'):
                        b.append('TRUE')
                    if (eval1[0]=='TRUE') and (eval2[0]=='UNDEF'):
                        b.append('UNDEF')
                    if (eval1[0]=='UNDEF') and (eval2[0]=='TRUE'):
                        b.append('UNDEF')
                    if (eval1[0]=='UNDEF') and (eval2[0]=='UNDEF'):
                        b.append('UNDEF')
                    b.append('LOGIC')
                    return b

            if expr[1] == '/.':
                eval1 = self.eval(expr[2])
                eval2 = self.eval(expr[3])
               
                b=[]
                if (type(eval1) is int or eval1[1]=='NUMERIC') and (eval2[1]=='LOGIC'):
                    if (eval2[0]=='TRUE'):
                        eval2=1
                    elif (eval2[0]=='FALSE'):
                        eval2=0
                    if type(eval2) is int and type(eval1) is int:
                        b.append(eval1/eval2)
                    elif type(eval2) is int and not type(eval1) is int:
                        if eval1[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval1[0]/eval2)
                    
                    elif not type(eval2) is int and type(eval1) is int:
                        if eval2[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval2[0]/eval1)
                    elif not type(eval2) is int and not type(eval1) is int:
                        if eval1[0]=='UNDEF' or eval2[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval1[0]/eval2[0])
                    b.append('NUMERIC')
                    return b
                if (eval1[1]=='LOGIC') and (type(eval2) is int or eval2[1]=='NUMERIC') :
                    if(type(eval2) is int):
                        
                        if(eval2>=0):
                            eva2=[]
                            eva2.append('TRUE')
                        else:
                            eva2=[]
                            eva2.append('FALSE')
                    else:
                        
                        
                        if ((eval2[0])=='UNDEF'):
                            eva2=[]
                            eva2.append('UNDEF')
                        elif ((eval2[0])>=0):
                            eva2=[]
                            eva2.append('TRUE')
                        elif ((eval2[0])<0):
                            eva2=[]
                            eva2.append('FALSE')
                        
                    
                    if (eval1[0]=='FALSE') and (eva2[0]=='FALSE'):
                        b.append('TRUE')
                    if (eval1[0]=='FALSE') and (eva2[0]=='TRUE'):
                        b.append('TRUE')
                    if (eval1[0]=='TRUE') and (eva2[0]=='FALSE'):
                        b.append('TRUE')
                    if (eval1[0]=='TRUE') and (eva2[0]=='TRUE'):
                        b.append('FALSE')
                    if (eval1[0]=='FALSE') and (eva2[0]=='UNDEF'):
                        b.append('TRUE')
                    if (eval1[0]=='UNDEF') and (eva2[0]=='FALSE'):
                        b.append('TRUE')
                    if (eval1[0]=='TRUE') and (eva2[0]=='UNDEF'):
                        b.append('UNDEF')
                    if (eval1[0]=='UNDEF') and (eva2[0]=='TRUE'):
                        b.append('UNDEF')
                    if (eval1[0]=='UNDEF') and (eva2[0]=='UNDEF'):
                        b.append('UNDEF')
                    b.append('LOGIC')
                    
                    return b

            if expr[1] == './':
                eval1 = self.eval(expr[2])
                eval2 = self.eval(expr[3])
               
                b=[]
                if (type(eval2) is int or eval2[1]=='NUMERIC') and (eval1[1]=='LOGIC'):
                    if (eval1[0]=='TRUE'):
                        eval1=1
                    elif (eval1[0]=='FALSE'):
                        eval1=0
                    if type(eval2) is int and type(eval1) is int:
                        b.append(eval1/eval2)
                    elif type(eval2) is int and not type(eval1) is int:
                        if eval1[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval1[0]/eval2)
                    
                    elif not type(eval2) is int and type(eval1) is int:
                        if eval2[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval2[0]/eval1)
                    elif not type(eval2) is int and not type(eval1) is int:
                        if eval1[0]=='UNDEF' or eval2[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval1[0]/eval2[0])
                    b.append('NUMERIC')
                    return b
                if (eval2[1]=='LOGIC') and (type(eval1) is int or eval1[1]=='NUMERIC') :
                    if(type(eval1) is int):
                        
                        if(eval1>=0):
                            eva1=[]
                            eva1.append('TRUE')
                        else:
                            eva1=[]
                            eva1.append('FALSE')
                    else:
                        if ((eval1[0])=='UNDEF'):
                            eva1=[]
                            eva1.append('UNDEF')
                        elif ((eval1[0])>=0):
                            eva1=[]
                            eva1.append('TRUE')
                        elif ((eval1[0])<0):
                            eva1=[]
                            eva1.append('FALSE')
                        
                    
                    if (eva1[0]=='FALSE') and (eval2[0]=='FALSE'):
                        b.append('TRUE')
                    if (eva1[0]=='FALSE') and (eval2[0]=='TRUE'):
                        b.append('TRUE')
                    if (eva1[0]=='TRUE') and (eval2[0]=='FALSE'):
                        b.append('TRUE')
                    if (eva1[0]=='TRUE') and (eval2[0]=='TRUE'):
                        b.append('FALSE')
                    if (eva1[0]=='FALSE') and (eval2[0]=='UNDEF'):
                        b.append('TRUE')
                    if (eva1[0]=='UNDEF') and (eval2[0]=='FALSE'):
                        b.append('TRUE')
                    if (eva1[0]=='TRUE') and (eval2[0]=='UNDEF'):
                        b.append('UNDEF')
                    if (eva1[0]=='UNDEF') and (eval2[0]=='TRUE'):
                        b.append('UNDEF')
                    if (eva1[0]=='UNDEF') and (eval2[0]=='UNDEF'):
                        b.append('UNDEF')
                    b.append('LOGIC')
                    
                    return b


                
            elif expr[1] == '^':
                eval1 = self.eval(expr[2])
                eval2 = self.eval(expr[3])
                b=[]
                if (type(eval1) is int or eval1[1]=='NUMERIC') and (type(eval2) is int or eval2[1]=='NUMERIC'):
                    if type(eval2) is int and type(eval1) is int:
                        b.append(eval1**eval2)
                    elif type(eval2) is int and not type(eval1) is int:
                        if eval1[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval1[0]**eval2)
                    
                    elif not type(eval2) is int and type(eval1) is int:
                        if eval2[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval2[0]**eval1)
                    elif not type(eval2) is int and not type(eval1) is int:
                        if eval1[0]=='UNDEF' or eval2[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval1[0]**eval2[0])
                    b.append('NUMERIC')
                    return b
                if (eval1[1]=='LOGIC') and (eval2[1]=='LOGIC'):
                    
                    if (eval1[0]=='FALSE') and (eval2[0]=='FALSE'):
                        b.append('TRUE')
                    if (eval1[0]=='FALSE') and (eval2[0]=='TRUE'):
                        b.append('FALSE')
                    if (eval1[0]=='TRUE') and (eval2[0]=='FALSE'):
                        b.append('FALSE')
                    if (eval1[0]=='TRUE') and (eval2[0]=='TRUE'):
                        b.append('FALSE')
                    if (eval1[0]=='FALSE') and (eval2[0]=='UNDEF'):
                        b.append('UNDEF')
                    if (eval1[0]=='UNDEF') and (eval2[0]=='FALSE'):
                        b.append('UNDEF')
                    if (eval1[0]=='TRUE') and (eval2[0]=='UNDEF'):
                        b.append('FALSE')
                    if (eval1[0]=='UNDEF') and (eval2[0]=='TRUE'):
                        b.append('FALSE')
                    if (eval1[0]=='UNDEF') and (eval2[0]=='UNDEF'):
                        b.append('UNDEF')
                    b.append('LOGIC')
                    return b
            elif expr[1] == '^.':
                eval1 = self.eval(expr[2])
                eval2 = self.eval(expr[3])
               
                b=[]
                if (type(eval1) is int or eval1[1]=='NUMERIC') and (eval2[1]=='LOGIC'):
                    if (eval2[0]=='TRUE'):
                        eval2=1
                    elif (eval2[0]=='FALSE'):
                        eval2=0
                    if type(eval2) is int and type(eval1) is int:
                        b.append(eval1**eval2)
                    elif type(eval2) is int and not type(eval1) is int:
                        if eval1[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval1[0]**eval2)
                    
                    elif not type(eval2) is int and type(eval1) is int:
                        if eval2[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval2[0]**eval1)
                    elif not type(eval2) is int and not type(eval1) is int:
                        if eval1[0]=='UNDEF' or eval2[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval1[0]**eval2[0])
                    b.append('NUMERIC')
                    return b
                if (eval1[1]=='LOGIC') and (type(eval2) is int or eval2[1]=='NUMERIC') :
                    if(type(eval2) is int):
                        
                        if(eval2>=0):
                            eva2=[]
                            eva2.append('TRUE')
                        else:
                            eva2=[]
                            eva2.append('FALSE')
                    else:
                        
                        
                        if ((eval2[0])=='UNDEF'):
                            eva2=[]
                            eva2.append('UNDEF')
                        elif ((eval2[0])>=0):
                            eva2=[]
                            eva2.append('TRUE')
                        elif ((eval2[0])<0):
                            eva2=[]
                            eva2.append('FALSE')
                        
                    
                    if (eval1[0]=='FALSE') and (eva2[0]=='FALSE'):
                        b.append('TRUE')
                    if (eval1[0]=='FALSE') and (eva2[0]=='TRUE'):
                        b.append('FALSE')
                    if (eval1[0]=='TRUE') and (eva2[0]=='FALSE'):
                        b.append('FALSE')
                    if (eval1[0]=='TRUE') and (eva2[0]=='TRUE'):
                        b.append('FALSE')
                    if (eval1[0]=='FALSE') and (eva2[0]=='UNDEF'):
                        b.append('UNDEF')
                    if (eval1[0]=='UNDEF') and (eva2[0]=='FALSE'):
                        b.append('UNDEF')
                    if (eval1[0]=='TRUE') and (eva2[0]=='UNDEF'):
                        b.append('FALSE')
                    if (eval1[0]=='UNDEF') and (eva2[0]=='TRUE'):
                        b.append('FALSE')
                    if (eval1[0]=='UNDEF') and (eva2[0]=='UNDEF'):
                        b.append('UNDEF')
                    b.append('LOGIC')
                    
                    return b

            elif expr[1] == '.^':
                eval1 = self.eval(expr[2])
                eval2 = self.eval(expr[3])
               
                b=[]
                if (type(eval2) is int or eval2[1]=='NUMERIC') and (eval1[1]=='LOGIC'):
                    if (eval1[0]=='TRUE'):
                        eval1=1
                    elif (eval1[0]=='FALSE'):
                        eval1=0
                    if type(eval2) is int and type(eval1) is int:
                        b.append(eval1**eval2)
                    elif type(eval2) is int and not type(eval1) is int:
                        if eval1[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval1[0]**eval2)
                    
                    elif not type(eval2) is int and type(eval1) is int:
                        if eval2[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval2[0]**eval1)
                    elif not type(eval2) is int and not type(eval1) is int:
                        if eval1[0]=='UNDEF' or eval2[0]=='UNDEF':
                            b.append('UNDEF')
                        else:
                            b.append(eval1[0]**eval2[0])
                    b.append('NUMERIC')
                    return b
                if (eval2[1]=='LOGIC') and (type(eval1) is int or eval1[1]=='NUMERIC') :
                    if(type(eval1) is int):
                        
                        if(eval1>=0):
                            eva1=[]
                            eva1.append('TRUE')
                        else:
                            eva1=[]
                            eva1.append('FALSE')
                    else:
                        if ((eval1[0])=='UNDEF'):
                            eva1=[]
                            eva1.append('UNDEF')
                        elif ((eval1[0])>=0):
                            eva1=[]
                            eva1.append('TRUE')
                        elif ((eval1[0])<0):
                            eva1=[]
                            eva1.append('FALSE')
                        
                    
                    if (eva1[0]=='FALSE') and (eval2[0]=='FALSE'):
                        b.append('TRUE')
                    if (eva1[0]=='FALSE') and (eval2[0]=='TRUE'):
                        b.append('FALSE')
                    if (eva1[0]=='TRUE') and (eval2[0]=='FALSE'):
                        b.append('FALSE')
                    if (eva1[0]=='TRUE') and (eval2[0]=='TRUE'):
                        b.append('FALSE')
                    if (eva1[0]=='FALSE') and (eval2[0]=='UNDEF'):
                        b.append('UNDEF')
                    if (eva1[0]=='UNDEF') and (eval2[0]=='FALSE'):
                        b.append('UNDEF')
                    if (eva1[0]=='TRUE') and (eval2[0]=='UNDEF'):
                        b.append('FALSE')
                    if (eva1[0]=='UNDEF') and (eval2[0]=='TRUE'):
                        b.append('FALSE')
                    if (eva1[0]=='UNDEF') and (eval2[0]=='UNDEF'):
                        b.append('UNDEF')
                    b.append('LOGIC')
                    
                    return b
    

        
        
        elif etype == 'VAR':
            var, dim1, dim2 = expr[1]
            if not dim1 and not dim2:
                if var in self.vars:
                    return self.vars[var]
                else:
                    print("UNDEFINED VARIABLE %s AT LINE %s" %
                          (var, self.stat[self.pc]))
                    raise RuntimeError
            # May be a list lookup or a function evaluation
            if dim1 and not dim2:
                if var in self.functions:
                    # A function
                    return self.functions[var](dim1)
                else:
                    # A list evaluation
                    if var in self.lists:
                        dim1val = self.eval(dim1)
                        if dim1val < 1 or dim1val > len(self.lists[var]):
                            print("LIST INDEX OUT OF BOUNDS AT LINE %s" %
                                  self.stat[self.pc])
                            raise RuntimeError
                        return self.lists[var][dim1val - 1]
            if dim1 and dim2:
                if var in self.tables:
                    dim1val = self.eval(dim1)
                    dim2val = self.eval(dim2)
                    if dim1val < 1 or dim1val > len(self.tables[var]) or dim2val < 1 or dim2val > len(self.tables[var][0]):
                        print("TABLE INDEX OUT OUT BOUNDS AT LINE %s" %
                              self.stat[self.pc])
                        raise RuntimeError
                    return self.tables[var][dim1val - 1][dim2val - 1]
            print("UNDEFINED VARIABLE %s AT LINE %s" %
                  (var, self.stat[self.pc]))
            raise RuntimeError

    # Evaluate a relational expression
    def releval(self, expr):
        etype = expr[1]
        lhs = self.eval(expr[2])
        rhs = self.eval(expr[3])
        if (type(lhs) is int):
            s=[]
            s.append(lhs)
            s.append('NUMERIC')
            lhs=s
        elif(lhs=='TRUE'):
            s=[]
            s.append(lhs)
            s.append('LOGIC')
            lhs=s
        elif(lhs=='TRUE'):
            s=[]
            s.append(lhs)
            s.append('LOGIC')
            lhs=s
        elif(lhs=='UNDEF'):
            s=[]
            s.append(lhs)
            lhs=s

        if (type(rhs) is int):
            s=[]
            s.append(rhs)
            s.append('NUMERIC')
            rhs=s
        elif(rhs=='TRUE'):
            s=[]
            s.append(rhs)
            s.append('LOGIC')
            rhs=s
        elif(rhs=='TRUE'):
            s=[]
            s.append(rhs)
            s.append('LOGIC')
            rhs=s
        elif(rhs=='UNDEF'):
            s=[]
            s.append(rhs)
            rhs=s


        if(lhs[0]=='UNDEF' or lhs[1]=='NUMERIC')and(rhs[0]=='UNDEF' or rhs[1]=='NUMERIC'):
            if etype == '<':
                if (lhs[0]=='UNDEF' or rhs[0]=='UNDEF'):
                    return 'FALSE'
                else:
                    if lhs[0] < rhs[0]:
                        return 'TRUE'
                    else:
                        return 'FALSE'

            elif etype == '>':
                if (lhs[0]=='UNDEF' or rhs[0]=='UNDEF'):
                    return 'FALSE'
                else:
                    if lhs[0] > rhs[0]:
                        return 'TRUE'
                    else:
                        return 'FALSE'

            elif etype == '?':
                if lhs[0] == rhs[0]:
                        return 'TRUE'
                else:
                        return 'FALSE'

            elif etype == '!':
                if lhs[0] != rhs[0]:
                        return 'TRUE'
                else:
                        return 'FALSE'

        if(lhs[0]=='UNDEF' or lhs[1]=='LOGIC')and(rhs[0]=='UNDEF' or rhs[1]=='LOGIC'):
            if etype == '<':
                if (lhs[0]=='UNDEF' or rhs[0]=='UNDEF'):
                    return 'FALSE'
                else:
                    if lhs[0]=='FALSE' and rhs[0]=='TRUE':
                        return 'TRUE'
                    else:
                        return 'FALSE'

            elif etype == '>':
                if (lhs[0]=='UNDEF' or rhs[0]=='UNDEF'):
                    return 'FALSE'
                else:
                    if lhs[0]=='TRUE' and rhs[0]=='FALSE':
                        return 'TRUE'
                    else:
                        return 'FALSE'

            elif etype == '?':
                if lhs[0]==rhs[0]:
                        return 'TRUE'
                else:
                        return 'FALSE'

            elif etype == '!':
                if lhs[0] != rhs[0]:
                        return 'TRUE'
                else:
                        return 'FALSE' 
 
        if(lhs[0]=='UNDEF' or lhs[1]=='NUMERIC')and(rhs[0]=='UNDEF' or rhs[1]=='LOGIC'):
            if (rhs[0]=='TRUE'):
                    rh=1
            elif (rhs[0]=='FALSE'):
                    rh=0
            elif (rhs[0]=='UNDEF'):
                    rh='UNDEF'
            if etype == '<.':
                if (lhs[0]=='UNDEF' or rh=='UNDEF'):
                    return 'FALSE'
                else:
                    if lhs[0] < rh:
                        return 'TRUE'
                    else:
                        return 'FALSE'

            elif etype == '>.':
                if (lhs[0]=='UNDEF' or rh=='UNDEF'):
                    return 'FALSE'
                else:
                    if lhs[0] > rh:
                        return 'TRUE'
                    else:
                        return 'FALSE'

            elif etype == '?.':
                if lhs[0] == rh:
                        return 'TRUE'
                else:
                        return 'FALSE'

            elif etype == '!.':
                if lhs[0] != rh:
                        return 'TRUE'
                else:
                        return 'FALSE'  


        if(lhs[0]=='UNDEF' or lhs[1]=='LOGIC')and(rhs[0]=='UNDEF' or rhs[1]=='NUMERIC'):
            if (rhs[0]>0):
                    rh='TRUE'
            elif (rhs[0]<=0):
                    rh='FALSE'
            elif (rhs[0]=='UNDEF'):
                    rh='FALSE'
            if etype == '<.':
                if (lhs[0]=='UNDEF' or rh=='UNDEF'):
                    return 'FALSE'
                else:
                    if lhs[0]=='FALSE' and rh=='TRUE':
                        return 'TRUE'
                    else:
                        return 'FALSE'

            elif etype == '>.':
                if (lhs[0]=='UNDEF' or rh=='UNDEF'):
                    return 'FALSE'
                else:
                    if lhs[0]=='TRUE' and rh=='FALSE':
                        return 'TRUE'
                    else:
                        return 'FALSE'

            elif etype == '?.':
                if lhs[0]==rh:
                        return 'TRUE'
                else:
                        return 'FALSE'

            elif etype == '!.':
                if lhs[0] != rh:
                        return 'TRUE'
                else:
                        return 'FALSE'         





        if(lhs[0]=='UNDEF' or lhs[1]=='LOGIC')and(rhs[0]=='UNDEF' or rhs[1]=='NUMERIC'):
            if (lhs[0]=='TRUE'):
                    lh=1
            elif (lhs[0]=='FALSE'):
                    lh=0
            elif (lhs[0]=='UNDEF'):
                    lh='UNDEF'
            if etype == '.<':
                if (lh=='UNDEF' or rhs[0]=='UNDEF'):
                    return 'FALSE'
                else:
                    if lh < rhs[0]:
                        return 'TRUE'
                    else:
                        return 'FALSE'

            elif etype == '.>':
                if (lh=='UNDEF' or rhs[0]=='UNDEF'):
                    return 'FALSE'
                else:
                    if lh > rhs[0]:
                        return 'TRUE'
                    else:
                        return 'FALSE'

            elif etype == '.?':
                if lh == rhs[0]:
                        return 'TRUE'
                else:
                        return 'FALSE'

            elif etype == '.!':
                if lh != rhs[0]:
                        return 'TRUE'
                else:
                        return 'FALSE'  


        if(lhs[0]=='UNDEF' or lhs[1]=='NUMERIC')and(rhs[0]=='UNDEF' or rhs[1]=='LOGIC'):
            if (lhs[0]>0):
                    lh='TRUE'
            elif (lhs[0]<=0):
                    lh='FALSE'
            elif (lhs[0]=='UNDEF'):
                    lh='UNDEF'
            if etype == '.<':
                if (lh=='UNDEF' or rhs[0]=='UNDEF'):
                    return 'FALSE'
                else:
                    if lh=='FALSE' and rhs[0]=='TRUE':
                        return 'TRUE'
                    else:
                        return 'FALSE'

            elif etype == '.>':
                if (lh=='UNDEF' or rhs[0]=='UNDEF'):
                    return 'FALSE'
                else:
                    if lh=='TRUE' and rhs[0]=='FALSE':
                        return 'TRUE'
                    else:
                        return 'FALSE'

            elif etype == '.?':
                if lh==rhs[0]:
                        return 'TRUE'
                else:
                        return 'FALSE'

            elif etype == '.!':
                if lh != rhs[0]:
                        return 'TRUE'
                else:
                        return 'FALSE'

    # Assignment
    def assign(self, target, value,types):
        var, dim1, dim2 = target
        if not dim1 and not dim2:
            s=[]
            a=self.eval(value)
            if not type(a) is int:
                if(a=='TRUE' or a=='FALSE' or a=='UNDEF'):
                    s.append(a)
                else:
                    s.append(a[0])

                
            else:
                s.append(a)
            s.append(types)
            self.vars[var] = s
        elif dim1 and not dim2:
            # List assignment
            dim1val = self.eval(dim1)
            if not var in self.lists:
                self.lists[var] = [0] * 10

            if dim1val > len(self.lists[var]):
                print ("DIMENSION TOO LARGE AT LINE %s" % self.stat[self.pc])
                raise RuntimeError
            self.lists[var][dim1val - 1] = self.eval(value)
        elif dim1 and dim2:
            dim1val = self.eval(dim1)
            dim2val = self.eval(dim2)
            if not var in self.tables:
                temp = [0] * 10
                v = []
                for i in range(10):
                    v.append(temp[:])
                self.tables[var] = v
            # Variable already exists
            if dim1val > len(self.tables[var]) or dim2val > len(self.tables[var][0]):
                print("DIMENSION TOO LARGE AT LINE %s" % self.stat[self.pc])
                raise RuntimeError
            self.tables[var][dim1val - 1][dim2val - 1] = self.eval(value)

    # Change the current line number
    def goto(self, linenum):
        if not linenum in self.prog:
            print("UNDEFINED LINE NUMBER %d AT LINE %d" %
                  (linenum, self.stat[self.pc]))
            raise RuntimeError
        self.pc = self.stat.index(linenum)


    def run(self):
        self.vars = {}            # All variables
        self.functions = {}
        self.procs = {}
        self.lists = {}            # List variables
        self.tables = {}            # Tables
        self.loops = []            # Currently active loops
        self.loopend = {}            # Mapping saying where loops end
        self.gosub = None           # Gosub return point (if any)
        self.error = 0              # Indicates program error

        self.stat = list(self.prog)  # Ordered list of all line numbers
        self.stat.sort()
        self.pc = 0                  # Current program counter

        # Processing prior to running

        self.collect_data()          # Collect all of the data statements
        self.check_end()

        if self.error:
            raise RuntimeError
        for line in self.prog.values():
            if line is None:
                continue
            # print(self.vars)
            self.ex(line)



    def ex(self,instr):
        if 1:
            if instr[0] == 'RECORD':
                if len(instr) == 3:
                    op = instr[0]
                    tname = instr[1]
                    param = instr[2]
                    s = []
                    k = []
                    i = 0
                   # s.append(instr[1])
                    while i < len(instr[2]):
                        a = []
                        self.ex(instr[2][i])
                        a.append(instr[2][i][1][0])
                        a.append(self.vars[instr[2][i][1][0]])
                        i = i + 1
                        k.append(a)
                   # a.append(self.vars[instr[2][1]])
                    s.append(k)
                    s.append(instr[0])
                    self.functions[tname] = s

                elif len(instr)==4:
                    if instr[1] == 'TO':
                        if instr[3][1] in self.functions:
                            tname = self.functions[instr[3][0]]

            else:
                op = instr[0]


            # PRINT statement
            if op == 'PRINT':
                plist = instr[1]
                out = ""
                for label, val in plist:
                    if out:
                        out += ' ' * (15 - (len(out) % 15))
						
                    out += label
                    if val:
                        if label:
                            out += " "
                        eval = self.eval(val)
            
                        out += str(eval[0])
                sys.stdout.write(out)
                end = instr[2]
                if not (end == ',' or end == ';'):
                    sys.stdout.write("\n")
                if end == ',':
                    sys.stdout.write(" " * (15 - (len(out) % 15)))
                if end == ';':
                    sys.stdout.write(" " * (3 - (len(out) % 3)))

					

            # VARIABLE statement
            elif op == 'NUMERIC':
                target = instr[1]
                value='UNDEF'
                self.assign(target, value, op)

            elif op == 'LOGIC':
                target = instr[1]
                value='UNDEF'
                self.assign(target, value, op)

            elif op == 'ASSIGN':
                target = instr[1]
                value = instr[2]
                if instr[1][0] in self.vars:
                    s = []
                    if (not value[0]=='UNARY') and (type(self.eval(value)) is int or self.eval(value)=='TRUE' or self.eval(value)=='FALSE'):

                        s.append(self.eval(value))
                        s.append(self.vars[instr[1][0]][1])
                        self.vars[instr[1][0]] = s

                    else:
                        self.vars[instr[1][0]] = self.eval(value)

                    for key, value in self.functions.items():
                        i = 0
                        while i < len(value[0]):
                            if instr[1][0] in value[0][i][0]:
                                self.functions[key][0][i][1] = s
                            i += 1
                else:
                    print("UNDEFINED VARIABLE %s" % instr[1][0])
                    raise RuntimeError

            # READ statement
            elif op == 'STATGROUP':
                self.ex(instr[1])
                if len(instr) == 3:
                    self.ex(instr[2])



            elif op == 'WHILE':
                loopvar = instr[1]
                initval = instr[2]
                a=len(initval)
                while(self.releval(loopvar)=='TRUE'):
                    self.ex(initval)
                    

            elif op == 'PROC':
                if instr[1] in self.procs:
                    init = self.procs[instr[1]]
                    self.ex(init[1])
                else:
                    fname = instr[1]
                    pname = instr[2]
                    s=[]
                    s.append(fname)
                    s.append(pname)
                    self.functions[fname] = s

            self.pc += 1

   
    def expr_str(self, expr):
        etype = expr[0]
        if etype == 'NUM':
            return str(expr[1])
        elif etype == 'GROUP':
            return "(%s)" % self.expr_str(expr[1])
        elif etype == 'UNARY':
            if expr[1] == '-':
                return "-" + str(expr[2])
        elif etype == 'BINOP':
            return "%s %s %s" % (self.expr_str(expr[2]), expr[1], self.expr_str(expr[3]))
        elif etype == 'VAR':
            return self.var_str(expr[1])

    def relexpr_str(self, expr):
        return "%s %s %s" % (self.expr_str(expr[2]), expr[1], self.expr_str(expr[3]))

    def var_str(self, var):
        varname, dim1, dim2 = var
        if not dim1 and not dim2:
            return varname
        if dim1 and not dim2:
            return "%s(%s)" % (varname, self.expr_str(dim1))
        return "%s(%s,%s)" % (varname, self.expr_str(dim1), self.expr_str(dim2))

    # Create a program listing
    def list(self):
        stat = list(self.prog)      # Ordered list of all line numbers
        stat.sort()
        for line in stat:
            instr = self.prog[line]
            op = instr[0]
            if op in ['END', 'STOP', 'RETURN']:
                print("%s %s" % (line, op))
                continue
            elif op == 'REM':
                print("%s %s" % (line, instr[1]))
            elif op == 'PRINT':
                _out = "%s %s " % (line, op)
                first = 1
                for p in instr[1]:
                    if not first:
                        _out += ", "
                    if p[0] and p[1]:
                        _out += '"%s"%s' % (p[0], self.expr_str(p[1]))
                    elif p[1]:
                        _out += self.expr_str(p[1])
                    else:
                        _out += '"%s"' % (p[0],)
                    first = 0
                if instr[2]:
                    _out += instr[2]
                print(_out)
            elif op == 'NUMERIC':
                print("%s NUMERIC %s = %s" %
                      (line, self.var_str(instr[1]), self.expr_str(instr[2])))
            elif op == 'READ':
                _out = "%s READ " % line
                first = 1
                for r in instr[1]:
                    if not first:
                        _out += ","
                    _out += self.var_str(r)
                    first = 0
                print(_out)
            elif op == 'IF':
                print("%s IF %s THEN %d" %
                      (line, self.relexpr_str(instr[1]), instr[2]))
            elif op == 'GOTO' or op == 'GOSUB':
                print("%s %s %s" % (line, op, instr[1]))
            elif op == 'FOR':
                _out = "%s FOR %s = %s TO %s" % (
                    line, instr[1], self.expr_str(instr[2]), self.expr_str(instr[3]))
                if instr[4]:
                    _out += " STEP %s" % (self.expr_str(instr[4]))
                print(_out)
            elif op == 'NEXT':
                print("%s NEXT %s" % (line, instr[1]))
            elif op == 'FUNC':
                print("%s DEF %s(%s) = %s" %
                      (line, instr[1], instr[2], self.expr_str(instr[3])))
            elif op == 'DIM':
                _out = "%s DIM " % line
                first = 1
                for vname, x, y in instr[1]:
                    if not first:
                        _out += ","
                    first = 0
                    if y == 0:
                        _out += "%s(%d)" % (vname, x)
                    else:
                        _out += "%s(%d,%d)" % (vname, x, y)

                print(_out)
            elif op == 'DATA':
                _out = "%s DATA " % line
                first = 1
                for v in instr[1]:
                    if not first:
                        _out += ","
                    first = 0
                    _out += v
                print(_out)

    # Erase the current program
    def new(self):
        self.prog = {}

    # Insert statements
    def add_statements(self, prog):
        for line, stat in prog.items():
            self.prog[line] = stat

    # Delete a statement
    def del_line(self, lineno):
        try:
            del self.prog[lineno]
        except KeyError:
            pass
