# interactive.py

import string
from stapel import Interpreter

class Interactive:
    
    def __init__(self):
        self.interpreter = Interpreter()
        self.print_stack = True
        self.prompt = ">"
        
    def mainloop(self):
        while 1:
            print self.prompt,
            line = raw_input()
            self.process_line(line)

            if self.print_stack:
                print "stack:", self.interpreter.stack_repr()
            
    def process_line(self, line):
        self.interpreter.feed(line)
        self.interpreter.execute_all()
        