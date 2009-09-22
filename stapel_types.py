# stapel_types.py
# Custom types.

class Symbol:
    def __init__(self, s):
        self.data = s
    def __repr__(self):
        return ":" + self.data
    
class Word:
    def __init__(self):
        raise NotImplementedError, "abstract class"
    
class BuiltinWord(Word):
    # assumed to be a "stack transformer", i.e. it's based on a function
    # whose arguments are taken from the stack, and which returns a list
    # whose elements are pushed onto the stack.
    def __init__(self, f):
        self.f = f
    def __call__(self, interpreter):
        num_args = self.f.func_code.co_argcount
        args = reversed([interpreter.pop() for x in range(num_args)])
        result = self.f(*args)
        for x in result:
            interpreter.push(x)
            
class BuiltinWordSideFX(BuiltinWord):
    def __call__(self, interpreter):
        # handles pushing and popping itself
        self.f(interpreter)
    
class UserDefinedWord(Word):
    def __init__(self, words):
        self.words = words # should all be instances of subclasses of Cmd
    def __call__(self, interpreter):
        # prepend words to command stack, so they'll be executed next
        interpreter.cmdstack = self.words + interpreter.cmdstack
