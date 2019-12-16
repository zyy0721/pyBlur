from ast import *

#BINOP SYMBOLS

#UNARYOP SYMBOLS

#BOOLOP SYMBOLS

#CMPOP SYMBOLS

class fromASTtoCode(NodeVisitor):




def AST2Code(node, indentation = ' ' * 4, flagLineInfo = False):
    code = fromASTtoCode(indentation, flagLineInfo)
    code.visit(node)

    return ''.join(code.result)