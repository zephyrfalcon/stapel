# commands.py

import stapel_types

class Cmd:
    def __init__(self, token):
        raise NotImplementedError, "abstract class"
        
    # pushing a value is the default for most word types.
    def execute(self, interpreter):
        interpreter.push(self.data)

class CmdInteger(Cmd):
    def __init__(self, token):
        self.data = int(token)
    
class CmdName(Cmd):
    def __init__(self, token):
        self.data = token # store as-is
    def execute(self, interpreter):
        value = interpreter.namespace[self.data]
        if isinstance(value, stapel_types.Word):
            value(interpreter)
        else:
            interpreter.push(value)

class CmdSymbol(Cmd):
    def __init__(self, token):
        self.data = token[1:] # strip the leading ':'
    def execute(self, interpreter):
        s = stapel_types.Symbol(self.data)
        interpreter.push(s)
        