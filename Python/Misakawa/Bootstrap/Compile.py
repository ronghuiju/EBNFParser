#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 20:01:18 2017

@author: misakawa
"""

Compile = True
from .Ast import ast_for_stmts
from .Parser import Stmt, token
from ..ObjectRegex.Node import MetaInfo
from ..ErrorFamily import handle_error
from ..scalable.core import fn
parser = handle_error(Stmt.match)
template = \
"""
from Misakawa.ObjectRegex.Node import Ref, AstParser, SeqParser, LiteralParser, MetaInfo
import re
namespace     = globals()
recurSearcher = set()
token = {tokendef}
{define}
{parser_compile}
"""


def compile(ebnf_text, language_name):
    info = dict(raw = [], regex = [])
    stmts = parser(token.findall(ebnf_text), MetaInfo(), partial=False)
    res, tks, to_compile = ast_for_stmts(stmts, info)
#    print(res)
    tks = sorted(tks['raw'])[::-1] + tks['regex']
    tokendef = "re.compile('|'.join([{}]))".format(','.join(tks))
    astParser_compile = lambda name : f"{name}.compile(namespace, recurSearcher)"
    parser_compile = '\n'.join(fn.map(astParser_compile)(to_compile))
    define         = '\n'.join(res)
    return template.format(define = define, parser_compile = parser_compile, tokendef = tokendef)

      
