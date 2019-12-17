#!-*-coding:utf-8 -*-
import ast
from ast import Assign, Name, Call, Store, Load, Str, Num, List, Add, BinOp
from ast import Subscript, Slice, Attribute, GeneratorExp, comprehension
from ast import Compare, Mult
import random
import sys
import fromASTtoCode

from ast import Assign, Name, Call, Store, Load, Str, Num, List, Add, BinOp, If
from ast import Subscript, Slice, Attribute, GeneratorExp, comprehension
from ast import Compare, Mult

def string_random(minlen, maxlen):
    from pip._vendor.msgpack.fallback import xrange
    return ''.join(chr(random.randint(0x61, 0x7a))
                   for x in xrange(random.randint(minlen, maxlen)))


def import_random(name, rdname):
    return Assign(
        targets=[Name(id=rdname, ctx=Store())],
        value=Call(func=Name(id='__import__', ctx=Load()),
                   args=[Str(s=name),
                         Call(func=Name(id='globals', ctx=Load()), args=[],
                              keywords=[], starargs=None, kwargs=None),
                         Call(func=Name(id='locals', ctx=Load()), args=[],
                              keywords=[], starargs=None, kwargs=None),
                         List(elts=[], ctx=Load()), Num(n=-1)],
                   keywords=[], starargs=None, kwargs=None))

def string_blur(str):
    randstr = string_random(3, 10)

    table0 = [
        # '' -> ''
        lambda: Str(s=''),
    ]

    table1 = [
        # 'a' -> 'a'
        lambda x: Str(s=chr(x)),
        # 'a' -> chr(0x61)
        lambda x: Call(func=Name(id='chr', ctx=Load()), args=[Num(n=x)],
                       keywords=[], starargs=None, kwargs=None),
    ]

    table = [
        # 'abc' -> 'abc'
        lambda x: Str(s=x),
        # 'abc' -> 'a' + 'bc'
        lambda x: BinOp(left=Str(s=x[:len(x) / 2]),
                        op=Add(),
                        right=Str(s=x[len(x) / 2:])),
        # 'abc' -> 'cba'[::-1]
        lambda x: Subscript(value=Str(s=x[::-1]),
                            slice=Slice(lower=None, upper=None,
                                        step=Num(n=-1)),
                            ctx=Load()),
        # 'abc' -> ''.join(_x for _x in reversed('cba'))
        lambda x: Call(
            func=Attribute(value=Str(s=''), attr='join', ctx=Load()), args=[
                GeneratorExp(elt=Name(id=randstr, ctx=Load()), generators=[
                    comprehension(target=Name(id=randstr, ctx=Store()),
                                  iter=Call(func=Name(id='reversed',
                                                      ctx=Load()),
                                            args=[Str(s=x[::-1])],
                                            keywords=[], starargs=None,
                                            kwargs=None),
                                  ifs=[])])],
            keywords=[], starargs=None, kwargs=None),
    ]

    if not len(str):
        return random.choice(table0)()

    if len(str) == 1:
        return random.choice(table1)(ord(str))

    return random.choice(table)(str)

class Blur(ast.NodeTransformer):
    def __init__(self):
        ast.NodeTransformer.__init__(self)
        #imported modules
        self.imports = {}

        #global values
        self.globs = {}

        #local values
        self.locs = {}

        #inside a function
        self.indef = False

    def Blur_global(self, name):
        newname = string_random(3, 10)
        self.globs[name] = newname
        return newname
    
    def Blur_local(self, name):
        newname = string_random(3, 10)
        self.locs[name] = newname
        return newname

    def visit_Import(self, node):
        newname = self.Blur_global(node.names[0].name)
        self.imports[node.names[0].name] = newname

    def visit_If(self, node):
        if isinstance(node.test, Compare) and \
                isinstance(node.test.left, Name) and \
                node.test.left.id == '__name__':
            for x, y in self.imports.items():
                node.body.insert(0, import_random(x, y))
        node.test = self.visit(node.test)
        node.body = [self.visit(x) for x in node.body]
        node.orelse = [self.visit(x) for x in node.orelse]
        return node

    def visit_Str(self, node):
        return string_random(node.s)

    def visit_Num(self, node):
        d = random.randint(1, 256)
        return BinOp(left=BinOp(left=Num(node.n / d), op=Mult(),
                                right=Num(n=d)),
                     op=Add(), right=Num(node.n % d))

    def visit_Attribute(self, node):
        if isinstance(node.value, Name) and isinstance(node.value.ctx, Load):
            node.value = self.visit(node.value)
            return Call(func=Name(id='getattr', ctx=Load()), args=[
                Name(id=node.value.id, ctx=Load()), Str(s=node.attr)],
                        keywords=[], starargs=None, kwargs=None)
        node.value = self.visit(node.value)
        return node

    def visit_FunctionDef(self, node):
        self.indef = True
        self.locs = {}
        node.name = self.obfuscate_global(node.name)
        node.body = [self.visit(x) for x in node.body]
        self.indef = False
        return node

    def visit_Name(self, node):
        # obfuscate known globals
        if not self.indef and isinstance(node.ctx, Store) and \
                node.id in ('teamname', 'flag'):
            node.id = self.obfuscate_global(node.id)
        # elif self.indef:
        # if isinstance(node.ctx, Store):
        # node.id = self.obfuscate_local(node.id)
        # node.id = self.locs.get(node.id, node.id)
        node.id = self.globs.get(node.id, node.id)
        return node

    def visit_Module(self, node):
        node.body = [y for y in (self.visit(x) for x in node.body) if y]
        node.body = [y for y in (self.visit(x) for x in node.body) if y]
        return node

class GlobalVarBlur(ast.NodeTransformer):
    def __init__(self, globs):
        ast.NodeTransformer.__init__(self)
        self.globs = {}

    def visit_Name(self, node):
        node.id = self.globs.get(node.id, node.id)
        return node


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: python %s <pyfile>' % sys.argv[0])
        exit(0)

    if sys.argv[1] == '-':
        root = ast.parse(sys.stdin.read())
    else:
        root = ast.parse(open(sys.argv[1], 'rb').read())

    # obfuscate the AST
    obf = Blur()
    root = obf.visit(root)

    # resolve all global names
    root = GlobalVarBlur(obf.globs).visit(root)

    print(fromASTtoCode.to_source(root))

    