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



    #Statements
    def visit_Assert(self, node):

    def visit_Assign(self, node):

    def visit_AugAssign(self, node):   

    def visit_Break(self, node):
    
    def visit_ClassDef(self, node):
    
    def visit_Continue(self, node): 
    
    def visit_Delete(self, node):

    def visit_Expr(self, node):
    
    def visit_For(self, node):

    def visit_FunctionDef(self, node):

    def visit_Global(self, node):

    def visit_ImportFrom(self, node):

    def visit_Import(self, node):

    def visit_If(self, node):

    def visit_Nonlocal(self, node):

    def visit_Pass(self, node):

    def visit_Print(self, node):
    
    def visit_TryExcept(self, node):

    def visit_TryFinally(self, node):

    def visit_Return(self, node):
    
    def visit_Raise(self, node):

    def visit_While(self, node):

    def visit_With(self, node):
    
    #Expressions
    def generator_visit(left, right):

    def sequence_visit(left, right):

    def visit_Attribute(self, node):

    def visit_Bytes(self, node):

    def visit_BinOp(self, node):

    def visit_BoolOp(self, node):

    def visit_Compare(self, node):

    def visit_Call(self, node):

    def visit_Dict(self, node):

    def visit_DictComp(self, node):
    
    def visit_ExtSlice(self, node):

    def visit_Ellipsis(self, node):

    def visit_IfExp(self, node):

    def visit_Lamda(self, node):

    def visit_Name(self, node):

    def visit_Num(self, node):

    def visit_Repr(self, node):

    def visit_Subscript(self, node):

    def visit_Slice(self, node):

    def visit_Str(self, node):

    def visit_Starred(self, node):

    def visit_Tuple(self, node):

    def visit_UnaryOp(self, node):
        
    def visit_Yield(self, node):

    #Helper Util
    def visit_alias(self, node):
    def visit_arguments(self, node):
    def visit_comprehension(self, node):

    def visit_excepthandler(self, node):


def AST2Code(node, indentation = ' ' * 4, flagLineInfo = False):
    code = fromASTtoCode(indentation, flagLineInfo)
    code.visit(node)

    return ''.join(code.result)