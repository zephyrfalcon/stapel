# stapel.py

from __future__ import with_statement
import re
import string
#
import builtins
import commands
import stapel_types

def tokenize(data):
    tokens = []
    for line in data.split('\n'):
        line = line.strip()
        parts = line.split() # FIXME
        try:
            idx = parts.index('#')
        except ValueError:
            pass
        else:
            parts = parts[:idx]
        tokens.extend(parts)
    return tokens
    
re_integer = re.compile("^-?[0-9]+$")
re_symbol = re.compile("^:\S+$")
    
def parse_token(token):
    if re_integer.match(token):
        return commands.CmdInteger(token)
    elif re_symbol.match(token):
        return commands.CmdSymbol(token)
    else:
        return commands.CmdName(token)
    
def parse(tokens):
    return [parse_token(token) for token in tokens]
    

class Interpreter:
    
    def __init__(self):
        self.cmdstack = []
        self.datastack = [[]]
        self.storage = [] # used by dip, etc.
        self.namespace = {}
        
        self.paren_depth = 0
        self.recorded = []
        
        self.load_builtins()
        self.load_stdlib()
        
    def load_builtins(self):
        for name, value in builtins.builtins.items():
            if value.func_name.startswith('s_'):
                self.namespace[name] = stapel_types.BuiltinWord(value)
            elif value.func_name.startswith('i_'):
                self.namespace[name] = stapel_types.BuiltinWordSideFX(value)
            else:
                raise NotImplementedError, name
                
    def load_stdlib(self):
        # FIXME: path should be relative to path of stapel.py
        with open("stdlib.s") as f:
            data = f.read()
            self.feed(data)
            self.execute_all()
                
    def feed(self, s):
        """ Parse data, add words to command stack, but don't execute them 
            yet. """
        tokens = tokenize(s)
        words = parse(tokens)
        self.cmdstack.extend(words)
        
    def execute_all(self):
        while self.cmdstack:
            self.execute_next()
        
    def execute_next(self):
        w = self.cmdstack.pop(0)
        assert isinstance(w, commands.Cmd)
        self.execute_word(w)
        
    def execute_word(self, cmd):
        if self.paren_depth > 0:
            self.recorded.append(cmd)
            if cmd.data == '(':
                self.paren_depth += 1
            elif cmd.data == ')':
                self.paren_depth -= 1
                if self.paren_depth == 0:
                    self.finish_recording()
        else:
            cmd.execute(self)
            
    def finish_recording(self):
        w = stapel_types.UserDefinedWord(self.recorded[:-1])
        self.recorded = []
        self.push(w)
        
    def push(self, x):
        self.datastack[-1].append(x)
        
    def pop(self):
        return self.datastack[-1].pop()
    
    def stack_repr(self):
        reprs = [repr(x) for x in self.datastack[-1]]
        return string.join(reprs, " ")
    
        
if __name__ == "__main__":
    
    from interactive import Interactive
    
    interactive = Interactive()
    interactive.mainloop()
    