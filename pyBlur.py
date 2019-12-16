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


class GlobalVarBlur(ast.NodeTransformer):


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: python %s <your pyfile>' % sys.argv[0])
        exit(0)

    