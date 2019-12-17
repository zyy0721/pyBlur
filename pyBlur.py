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
    
    def Blur_local(self, name):

    def visit_Import(self, node):

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


    def visit_Str(self, node):

    def visit_Num(self, node):

    def visit_Attribute(self, node):

    def visit_FunctionDef(self, node):

    def visit_Name(self, node):

    def visit_Module(self, node):

class GlobalVarBlur(ast.NodeTransformer):
    def __init__(selff, globals):

    def visit_Name(self, node):
        


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: python %s <your pyfile>' % sys.argv[0])
        exit(0)

    