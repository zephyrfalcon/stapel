# test_stapel.py

import unittest
#
from stapel import Interpreter

TESTDATA = [
    ("1 2 3", "1 2 3"),
    ("4 5 +", "9"),
    ("4 5 -", "-1"),
    
    (":foo", ":foo"),
    (":x 3 define", ""),
    (":x 3 define x", "3"),
    
    ("( 1 2 3 ) exec", "1 2 3"),
    (":++ ( 1 + ) define   7 :++ ref exec", "8"),
    
    ("[ 1 2 3 ]", "[1, 2, 3]"),
    ("( 1 + ) [ 1 2 3 ] map", "[2, 3, 4]"),
    ("1 2 3 ( swap ) dip", "2 1 3"),
    ("1 2 3 ( drop ) dip", "1 3"),
    ("[ 1 2 3 ] uncons", "1 [2, 3]"),
    ("1 [ 2 3 ] cons", "[1, 2, 3]"),
    ("[ 1 2 3 ] 4 append", "[1, 2, 3, 4]"),
    ("[ 3 ] empty?", "False"),
    ("[ ] empty?", "True"),
    ("true 3 4 choice", "3"),
    ("false 3 4 choice", "4"),
    ("true ( 3 ) ( 4 ) if", "3"),
    ("1 2 3 dupd", "1 2 2 3"),
    ("1 2 3 swapd", "2 1 3"),
]

class TestStapel(unittest.TestCase):
    
    def setUp(self):
        self.interpreter = Interpreter()
        
# add methods to TestStapel dynamically
for idx, (cmds, stack) in enumerate(TESTDATA):
    def test_expr(self, cmds=cmds, stack=stack):
        self.interpreter.feed(cmds)
        self.interpreter.execute_all()
        self.assertEquals(self.interpreter.stack_repr(), stack)
    name = 'test_expr_%03d' % idx
    setattr(TestStapel, name, test_expr)
    
if __name__ == "__main__":
    unittest.main()
    