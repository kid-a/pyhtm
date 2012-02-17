#!/usr/bin/python
##------------------------------------------------------------------------------
## tests.py
## 
## Unit tests for pyhtm
##------------------------------------------------------------------------------
import unittest
import numpy

from pyhtm import *

EPSILON = 0.000001


class NodeTest(unittest.TestCase):

    def sample_data (self):
        ## sample data have the form (lambda-, C, PCG, lamba+)
        
        return { 'm' : ( {'one'   : array ([0.05, 0.30, 0.70, 0.02, 0.23]),
                          'two'   : array ([0.15, 0.02, 0.18, 0.4]),
                          'three' : array ([0.90, 0.02]),
                          'four'  : array ([0.10, 0.42, 0.15])},
                         
                         [{ 'one' : 5,
                            'two' : 3,
                            'three' : 1,
                            'four' : 1
                            },
                          
                          { 'one' : 2,
                            'two' : 2,
                            'three' : 1,
                            'four' : 1
                            },
                          ],
                         
                         ##transpose(array ([[5, 3, 1, 1],])),
                         array([[1], [1]]),
                         array([[1]]))
                 }
    
    def test_feed (self):
        n = Node ()
        (l_minus, C, PCG, l_plus) = self.sample_data ()['m']

        for l in l_minus.itervalues():
            n.feed(l[1], l[0])
            
        for l in l_minus.itervalues():
            self.assertEqual(n._lambda_minus[l[0]], l[1])
        

    def test_inference (self):
        n = Node ()
        (n._lambda_minus, n._C, n._PCG, n._lambda_plus) = \
            self.sample_data ()['m']
        
        n.inference ()
        
        ## assert on y vector
        for i in range (len (n._y)):            
            self.assertTrue ( abs(n._y[i] - array([[0.23 * 0.18 * 0.9 * 0.1],
                                                   [0.30 * 0.02 * 0.9 * 0.1]])[i]) <=
                              EPSILON )
            
        ## assert on lambda+ vector
        for i in range (len (n._lambda_plus)):
            self.assertTrue (abs (n._lambda_plus[i] - [[0.23 * 0.18 * 0.9 * 0.1],
                                                       [0.30 * 0.02 * 0.9 * 0.1]][i]))

##
##------------------------------------------------------------------------------
##  Main
##------------------------------------------------------------------------------
if __name__ == "__main__":
    unittest.main ()
