from ast import *

#BINOP SYMBOLS
BINOP_SYMBOLS = {}
BINOP_SYMBOLS[Add] = '+'
BINOP_SYMBOLS[Sub] = '-'
BINOP_SYMBOLS[Mult] = '*'
BINOP_SYMBOLS[Div] = '/'
BINOP_SYMBOLS[Mod] = '%'
BINOP_SYMBOLS[Pow] = '**'
BINOP_SYMBOLS[LShift] = '<<'
BINOP_SYMBOLS[RShift] = '>>'
BINOP_SYMBOLS[BitOr] = '|'
BINOP_SYMBOLS[BitXor] = '^'
BINOP_SYMBOLS[BitAnd] = '&'
BINOP_SYMBOLS[FloorDiv] = '//'

#UNARYOP SYMBOLS
UNARYOP_SYMBOLS = {}
UNARYOP_SYMBOLS[Invert] = '~'
UNARYOP_SYMBOLS[Not] = 'not'
UNARYOP_SYMBOLS[UAdd] = '+'
UNARYOP_SYMBOLS[USub] = '-'

#BOOLOP SYMBOLS
BOOLOP_SYMBOLS = {}
BOOLOP_SYMBOLS[And] = 'and'
BOOLOP_SYMBOLS[Or] = 'or'


#CMPOP SYMBOLS
CMPOP_SYMBOLS = {}
CMPOP_SYMBOLS[Eq] = '=='
CMPOP_SYMBOLS[NotEq] = '!='
CMPOP_SYMBOLS[Lt] = '<'
CMPOP_SYMBOLS[LtE] = '<='
CMPOP_SYMBOLS[Gt] = '>'
CMPOP_SYMBOLS[GtE] = '>='
CMPOP_SYMBOLS[Is] = 'is'
CMPOP_SYMBOLS[IsNot] = 'is not'
CMPOP_SYMBOLS[In] = 'in'
CMPOP_SYMBOLS[NotIn] = 'not in'

class fromASTtoCode(NodeVisitor):
    def __init__(self, indentation, flagLineInfo = False):
        self.indentation = indentation
        self.flagLineInfo = flagLineInfo
        self.result = []
        self.myIndent = 0
        self.newLines = 0

    def write(self, x):
        if self.new_lines:
            if self.result:
                self.result.append('\n' * self.new_lines)
            self.result.append(self.indent_with * self.indentation)
            self.new_lines = 0
        self.result.append(x)

    def newline(self, node=None, extra=0):
        self.new_lines = max(self.new_lines, 1 + extra)
        if node is not None and self.add_line_information:
            self.write('# line: %s' % node.lineno)
            self.new_lines = 1

    def body(self, statements):
        self.new_line = True
        self.indentation += 1
        for stmt in statements:
            self.visit(stmt)
        self.indentation -= 1

    def body_or_else(self, node):
        self.body(node.body)
        if node.orelse:
            self.newline()
            self.write('else:')
            self.body(node.orelse)

    def signature(self, node):
        want_comma = []
        def write_comma():
            if want_comma:
                self.write(', ')
            else:
                want_comma.append(True)

        padding = [None] * (len(node.args) - len(node.defaults))
        for arg, default in zip(node.args, padding + node.defaults):
            write_comma()
            self.visit(arg)
            if default is not None:
                self.write('=')
                self.visit(default)
        if node.vararg is not None:
            write_comma()
            self.write('*' + node.vararg)
        if node.kwarg is not None:
            write_comma()
            self.write('**' + node.kwarg)

    def decorators(self, node):
        for decorator in node.decorator_list:
            self.newline(decorator)
            self.write('@')
            self.visit(decorator)

    #Statements
    def visit_Assert(self, node):
        self.newline(node)
        self.write('assert ')
        self.visit(node.test)
        if node.msg is not None:
           self.write(', ')
           self.visit(node.msg)

    def visit_Assign(self, node):
        self.newline(node)
        for idx, target in enumerate(node.targets):
            if idx:
                self.write(', ')
            self.visit(target)
        self.write(' = ')
        self.visit(node.value)

    def visit_AugAssign(self, node):
        self.newline(node)
        self.visit(node.target)
        self.write(' ' + BINOP_SYMBOLS[type(node.op)] + '= ')
        self.visit(node.value)

    def visit_Break(self, node):
        self.newline(node)
        self.write('break')

    def visit_ClassDef(self, node):
        have_args = []

        def paren_or_comma():
            if have_args:
                self.write(', ')
            else:
                have_args.append(True)
                self.write('(')

        self.newline(extra=2)
        self.decorators(node)
        self.newline(node)
        self.write('class %s' % node.name)
        for base in node.bases:
            paren_or_comma()
            self.visit(base)
        # XXX: the if here is used to keep this module compatible
        #      with python 2.6.
        if hasattr(node, 'keywords'):
            for keyword in node.keywords:
                paren_or_comma()
                self.write(keyword.arg + '=')
                self.visit(keyword.value)
            if node.starargs is not None:
                paren_or_comma()
                self.write('*')
                self.visit(node.starargs)
            if node.kwargs is not None:
                paren_or_comma()
                self.write('**')
                self.visit(node.kwargs)
        self.write(have_args and '):' or ':')
        self.body(node.body)
    
    def visit_Continue(self, node):
        self.newline(node)
        self.write('continue')
    
    def visit_Delete(self, node):
        self.newline(node)
        self.write('del ')
        for idx, target in enumerate(node):
            if idx:
                self.write(', ')
            self.visit(target)

    def visit_Expr(self, node):
        self.newline(node)
        self.generic_visit(node)
    
    def visit_For(self, node):
        self.newline(node)
        self.write('for ')
        self.visit(node.target)
        self.write(' in ')
        self.visit(node.iter)
        self.write(':')
        self.body_or_else(node)

    def visit_FunctionDef(self, node):
        self.newline(extra=1)
        self.decorators(node)
        self.newline(node)
        self.write('def %s(' % node.name)
        self.visit(node.args)
        self.write('):')
        self.body(node.body)

    def visit_Global(self, node):
        self.newline(node)
        self.write('global ' + ', '.join(node.names))

    def visit_ImportFrom(self, node):
        self.newline(node)
        self.write('from %s%s import ' % ('.' * node.level, node.module))
        for idx, item in enumerate(node.names):
            if idx:
                self.write(', ')
            self.write(item)

    def visit_Import(self, node):
        self.newline(node)
        for item in node.names:
            self.write('import ')
            self.visit(item)

    def visit_If(self, node):
        self.newline(node)
        self.write('if ')
        self.visit(node.test)
        self.write(':')
        self.body(node.body)
        while True:
            else_ = node.orelse
            if len(else_) == 0:
                break
            elif len(else_) == 1 and isinstance(else_[0], If):
                node = else_[0]
                self.newline()
                self.write('elif ')
                self.visit(node.test)
                self.write(':')
                self.body(node.body)
            else:
                self.newline()
                self.write('else:')
                self.body(else_)
                break


    def visit_Nonlocal(self, node):
        self.newline(node)
        self.write('nonlocal ' + ', '.join(node.names))

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