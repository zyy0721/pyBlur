#!-*-coding:utf-8 -*-
import ast
import random
import sys

import fromASTtoCode

from ast import Assign, Name, Call, Store, Load, Str, Num, List, Add, BinOp
from ast import Subscript, Slice, Attribute, GeneratorExp, comprehension
from ast import Compare, Mult

def string_random(minlen, maxlen):
    return xxx

def import_random(name, rdname):
    return xxx

def string_blur(str):
    return xxx

class Blur(ast.NodeTransformer):
    def __init__(self):
        ast.NodeTransformer.__init__(self)
        #imported modules

        #global values

        #local values

        #inside a function

    def Blur_global(self, name):
    
    def Blur_local(self, name):

    def visit_Import(self, node):

    def visit_If(self, node):

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

    