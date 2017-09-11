#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 22:45:50 2017

@author: misakawa
"""

import re

from copy import deepcopy
class MetaInfo(dict):
    
    def __init__(self, count=0 , trace = None):
        self['count'] = count
        self['trace'] = trace if trace else []
        self['last_count'] = 0
    
    def merge(self, meta):

        self['count'] += meta['count']
        self['trace'] += meta['trace']
        
        return self
    
    @property
    def branch(self):
        return MetaInfo(count = self.count, trace = deepcopy(self['trace']))
    
    @property
    def last_count(self):
        return self['last_count']
    
    @last_count.setter
    def last_count(self, v):
        self['last_count'] += v
        return self
    
        
    
    @property
    def count(self):
        return self['count']
    
    @count.setter
    def count(self,v):
        self['count'] = v
        return self
    
    @property
    def trace(self):
        return self['trace']
    
    @trace.setter
    def trace(self,v):
        self['trace'] = v
        return self
    
    @property
    def clean(self):
        self.trace.clear()
        self.count = 0
        return self

    
    
    
def reMatch(x, make = lambda x:x, escape = False):
    
    re_ = re.compile( re.escape(x) if escape else x)
    def _1(ys):
        if not ys: return None
        r = re_.match(ys[0])
        if not r : return None
        a, b = r.span()
        if a!=0 : raise Exception('a is not 0')
        if b is not len(ys[0]):
            return None
        return  ys[0]
    return _1

class Liter:
    def __init__(self, i, name = None):
        self.f = reMatch(i)
        self.name = name
        self.has_recur = False
    def match(self, objs, meta_info = None, partial = True):
        if not meta_info: meta_info = MetaInfo()
        r = self.f(objs)
        if r:
            if partial or len(objs) == 1:
                meta_info.count += 1
                if r == '\n':
                    # for inplementation
                    pass
                return meta_info, r
            return None
        return None
    
class ELiter:
    def __init__(self, i, name = None):
        self.f = reMatch(i, escape = True)
        self.name = name
        self.has_recur = False
    def match(self, objs, meta_info = None, partial = True):
        if not meta_info: meta_info = MetaInfo()
        r = self.f(objs)
        if r:
            if partial or len(objs) == 1:
                meta_info.count += 1
                if r == '\n':
                    # for inplementation
                    pass
                return meta_info, r
            return None
        return None
    


class recur:
    def __init__(self, name):
        self.name = name


def redef(self, *args, **kwargs):
    self.__init__(*args, **kwargs)
    return self
    
class mode(list):
    def setName(self, name):
        self.name = name
        return self


    
        


class ast:
    def __init__(self, compile_closure, *ebnf, name = None):
        self.name     = name
        self.possibilities= []
        self.has_recur = False
        self.cache    = ebnf
        self.compile_closure = compile_closure
        self.compiled = False

    
    @property
    def compile(self):
        if self.compiled: return self
        for es in self.cache:
            self.possibilities.append([])
            for e in es:
                if e is recur:
                    self.possibilities[-1].append(self)
                    
                    if not self.has_recur:
                        self.has_recur = True
                elif isinstance(e, recur):
                    e = self.compile_closure[e.name]
                    self.possibilities[-1].append(e)
                    if not self.has_recur:
                        self.has_recur = e.has_recur
                elif isinstance(e, ast):
                    e.compile
                    self.possibilities[-1].append(e)
                    if not self.has_recur:
                        self.has_recur = e.has_recur
                else:
                    self.possibilities[-1].append(e)
        del self.cache
        self.compiled = True
        return self
        
    def match(self, objs, meta_info = None, partial = True):
        if not meta_info : 
            if self.has_recur:
                meta_info = MetaInfo() 
                meta_info.trace.append(self.name)
            else :
                meta_info = MetaInfo()
                                  
        res   = mode().setName(self.name)
        meta_info.count = 0 
        goto = False
        # debug
#        for i, possible in enumerate(self.possibilities):
        # ===
        
        for possible in self.possibilities:
            new_meta = meta_info.branch
            for i, thing in enumerate(possible):
                # eliminates the left recursion 
                
                print(f"<< {thing.name} >> {new_meta}")
                if i is 0:
#                    print(thing.name)
#                    print(meta_info)
                    if new_meta.last_count == new_meta.count and thing.name in meta_info.trace:
                        # debug
                        print("Found L-R! Dealed!")
                        # ===
                        res.clear()
                        new_meta = None
                        goto = True
                        break
                
                new_meta.last_count = new_meta.count
                r = thing.match(objs[new_meta.count:], meta_info=new_meta, partial = partial)
                
                # debug
                
                print(f"{self.name} <=", r[1] if isinstance(r, tuple) else r)
                print()
                # ===
                
                
                if not r:
                    # nexr possible
                    res.clear()
                    new_meta = None
                    goto = True
                    break
                
                a, b = r
                
#                if a.count is not 0:                    
#                    new_meta.merge(a)
                    
                    
                    
                
                if b:
                    if isinstance(thing, Seq):
                        res.extend(b)
                    else:
                        res.append(b)
            else:
                goto = False
                
            if goto : 
                # debug
#                print(f'{self.name} -goto from', thing.name)
                # ===
                continue
#            print(i)   
                    
            return (new_meta , res) if new_meta else None
                
                    
class Seq(ast):
    def __init__(self,compile_closure, *ebnf, name = None, atleast = 1):
        super(Seq, self).__init__(compile_closure, *ebnf, name = name)
        self.atleast = atleast
        
    def match(self, objs, meta_info=None, partial = True):
        if not meta_info : 
            if self.has_recur:
                meta_info = MetaInfo() 
                meta_info.trace.append(self.name)
            else :
                meta_info = MetaInfo()
                
        res = mode().setName(self.name)
        if not objs:
            if self.atleast is 0:
                return meta_info , None
            return None
        meta_info.count = 0
        
        # debug
#        i = 0
        # ===
        new_meta = meta_info.branch
        while True:
            
            # debug
#            i+=1
#            if i>20:raise
            # ===
            print('objs =>', objs[new_meta.count:])
            r = super(Seq, self).match(objs[new_meta.count:], meta_info = new_meta, partial = True)
            if not r:
                break

            a, b = r
            
            if b:
                res.extend(b)
            
            new_meta.merge(a)
            
            
        if len(res) < self.atleast:
            return  None
        print('res->',res)
        return new_meta, res
                
                    
                
            
    
                
            
    
    
    