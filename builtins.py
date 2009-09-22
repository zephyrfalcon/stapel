# builtins.py
#
# Note:
# Functions whose names start with 's_' are considered to be "stack
# transformers", i.e. they consume and produce a stack.
# Functions whose names start with 'i_' need access to the interpreter
# object, in addition to the stack.

import commands
import stapel_types

# some of these can be added to the stdlib instead...

def s_dup(x): return [x, x]
def s_drop(x): return []
def s_swap(a, b): return [b, a]
def s_over(a, b): return [a, b, a]
def s_ror(a, b, c): return [c, a, b]
def s_rol(a, b, c): return [b, c, a]
def s_nip(a, b): return [b]
def s_tuck(a, b): return [b, a, b]

def s_plus(a, b): return [a+b]
def s_minus(a, b): return [a-b]
def s_times(a, b): return [a*b]

def s_true(): return [True]
def s_false(): return [False]

def s_cons(a, b): return [[a] + b]
def s_uncons(lst): return [lst[0], lst[1:]]
def s_append(lst, x): return [lst+[x]]
def s_empty_p(lst): return [not bool(len(lst))]

def s_choice(cond, iftrue, iffalse):
    # NOT the same as if, which does delayed evaluation
    return [iftrue if cond else iffalse]

def i_stacklength(interpreter):
    sl = len(interpreter.datastack[-1])
    interpreter.push(sl)
    
def i_stackdepth(interpreter):
    sd = len(interpreter.datastack)
    interpreter.push(sd)
    
def i_lparen(interpreter):
    # switch interpreter to 'recording' mode, until matching rparen is found
    interpreter.paren_depth += 1

def i_exec(interpreter):
    """ ( word-definition -- ? ) """
    w = interpreter.pop()
    w(interpreter)
    
def i_define(interpreter):
    """ ( name value -- ) 
        Add a definition to the namespace. """
    value = interpreter.pop()
    name = interpreter.pop()
    assert isinstance(name, stapel_types.Symbol)
    interpreter.namespace[name.data] = value
    
def i_lbracket(interpreter):
    interpreter.datastack.append([])
    
def i_rbracket(interpreter):
    x = interpreter.datastack.pop()
    interpreter.push(x)
    
def i_ref(interpreter):
    """ ( symbol -- value ) """
    symbol = interpreter.pop()
    value = interpreter.namespace[symbol.data]
    interpreter.push(value)
    
def i_prc_dip(interpreter):
    x = interpreter.pop()
    interpreter.storage.append(x)
    
def i_prc_undip(interpreter):
    x = interpreter.storage.pop()
    interpreter.push(x)
    
def i_dip(interpreter):
    block = interpreter.pop()
    transform = [commands.CmdName('%dip')] + block.words + [commands.CmdName('%undip')]
    interpreter.cmdstack = transform + interpreter.cmdstack
    # hmm...
    # swap %dip exec %undip ...?

builtins = {
    "drop": s_drop,
    "dup": s_dup,
    "nip": s_nip,
    "over": s_over,
    "rol": s_rol,
    "ror": s_ror,
    "swap": s_swap,
    "tuck": s_tuck,
    
    "+": s_plus,
    "-": s_minus,
    "*": s_times,
    
    "true": s_true,
    "false": s_false,

    "append": s_append,
    "empty?": s_empty_p,
    "cons": s_cons,
    "uncons": s_uncons,
    
    "choice": s_choice,
    
    "(": i_lparen,
    "[": i_lbracket,
    "]": i_rbracket,
    "define": i_define,
    "dip": i_dip,
    "exec": i_exec,
    "ref": i_ref,
    "stackdepth": i_stackdepth,
    "stacklength": i_stacklength,
    
    # semi-private
    "%dip": i_prc_dip,
    "%undip": i_prc_undip,
}
