from ast import *

#BINOP SYMBOLS

#UNARYOP SYMBOLS

#BOOLOP SYMBOLS

#CMPOP SYMBOLS

class fromASTtoCode(NodeVisitor):
    def __init__(self, indentation, flagLineInfo = False):
        self.indentation = indentation
        self.flagLineInfo = flagLineInfo
        self.result = []
        self.myIndent = 0
        self.newLines = 0



def AST2Code(node, indentation = ' ' * 4, flagLineInfo = False):
    code = fromASTtoCode(indentation, flagLineInfo)
    code.visit(node)

    return ''.join(code.result)