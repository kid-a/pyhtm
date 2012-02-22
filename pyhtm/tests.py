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
        
        return { 'i' : ( 
                
                ## lambda_minus = 
                {'one'   : array ([0.05, 0.30, 0.70, 0.02, 0.23]),
                 'two'   : array ([0.15, 0.02, 0.18, 0.4]),
                 'three' : array ([0.90, 0.02]),
                 'four'  : array ([0.10, 0.42, 0.15])},
                
                ## coincidences = 
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
                
                ## PGC = 
                ## sum over columns must be == 1
                array([[0.7, 0.1], 
                       [0.3, 0.9]]),
                
                ## lambda_plus = 
                array([0.00277, 0.0008586])
                ),
                 
                 'e': (

                ## lambda_minus =
                array ([[0.3794282,  0.0507689,  0.7252412,  0.2874779],
                        [0.2169248,  0.8720986,  0.3372325,  0.9286008],
                        [0.2597954,  0.6256833,  0.6724002,  0.1137731],
                        [0.5740579,  0.0080139,  0.6572505,  0.2916554]]),
                
                ## coincidences =
                array([[0.061490,   0.097498,   0.987485,   0.921944,
                        0.608442,   0.812821,   0.685156,   0.963380,
                        0.923897,   0.887088,   0.683552,   0.683180,
                        0.244258,   0.963484,   0.220534,   0.925960],
                       
                       [0.417075,  0.836787,  0.953429,  0.076610,
                        0.490397,  0.573417,  0.903105,  0.372850,
                        0.209912,  0.067709,  0.358607,  0.553040,
                        0.126210,  0.489527,  0.864474,  0.576415]]),
                
                ## PCG = 
                array([[0.7, 0.1], 
                       [0.3, 0.9]]),
                
                ## lambda_plus = 
                array([0.00277, 0.0008586])
                )
                 }
    
    def test_feed_intermediate (self):
        n = Node ()
        (l_minus, C, PCG, l_plus) = self.sample_data ()['i']

        for l in l_minus.itervalues():
            n.feed(l[1], l[0])
            
        ## assert on lambda- vector
        for l in l_minus.itervalues():
            self.assertEqual(n._lambda_minus[l[0]], l[1])
        

    def test_inference_intermediate (self):
        n = Node ()
        (n._lambda_minus, n._C, n._PCG, lambda_plus) = \
            self.sample_data ()['i']
        
        n.inference ()
        
        ## assert on y vector
        for i in range (len (n._y)):            
            self.assertTrue ( abs(n._y[i] - array([[0.23 * 0.18 * 0.9 * 0.1],
                                                   [0.30 * 0.02 * 0.9 * 0.1]])[i]) <=
                              EPSILON )
            
        ## assert on lambda+ vector
        for i in range (len (lambda_plus)):
            self.assertTrue ( abs(n._lambda_plus[i] - lambda_plus[i]) - 
                              EPSILON )


    def test_feed_entry (self):
        n = EntryNode ()
        (l_minus, C, PCG, l_plus) = self.sample_data ()['e']
        
        n.feed (l_minus)
        self.assertEqual (n._lambda_minus.all (), l_minus.all ())

    def test_inference_entry (self):
        n = EntryNode ()
        (l_minus, C, PCG, l_plus) = self.sample_data ()['e']
        
        n.feed (l_minus)
        n._C = C
        n._PCG = PCG
        
        n.inference ()

        for i in range (len (n._y)):
            print n._y[i], [0.14134, 0.23658][i]
            self.assertTrue ( abs(n._y[i] - [0.036805, 0.069215][i]) <=
                              EPSILON )
##
##------------------------------------------------------------------------------
##  Main
##------------------------------------------------------------------------------
if __name__ == "__main__":
    unittest.main ()
