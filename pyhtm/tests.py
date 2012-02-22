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
        ## sample data have the form (lambda-, C, Y, PCG, lamba+)
        return { 
            ##------------------------------------------------------------------
            ## INTERMEDIATE NODE TEST DATA
            ##------------------------------------------------------------------
            'i' : ( 
                ## sLambdaMinus = 
                {'one'   : array ([0.05, 0.30, 0.70, 0.02, 0.23]),
                 'two'   : array ([0.15, 0.02, 0.18, 0.4]),
                 'three' : array ([0.90, 0.02]),
                 'four'  : array ([0.10, 0.42, 0.15])},
                
                ## sC = 
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
                
                ## sY =
                array([[0.23 * 0.18 * 0.9 * 0.1],
                       [0.30 * 0.02 * 0.9 * 0.1]]),
                
                ## sPGC = 
                ## (pay attention: sum over columns must be == 1)
                array([[0.7, 0.1], 
                       [0.3, 0.9]]),
                
                ## sLambdaPlus = 
                array([0.00277, 0.0008586])
                ),
            
            ##------------------------------------------------------------------
            ## ENTRY NODE TEST DATA
            ## -----------------------------------------------------------------
            'e': (
                ## sLambdaMinus =
                array ([[0.3794282,  0.0507689,  0.7252412,  0.2874779],
                        [0.2169248,  0.8720986,  0.3372325,  0.9286008],
                        [0.2597954,  0.6256833,  0.6724002,  0.1137731],
                        [0.5740579,  0.0080139,  0.6572505,  0.2916554]]),
                
                ## sC =
                array([[0.061490,   0.097498,   0.987485,   0.921944,
                        0.608442,   0.812821,   0.685156,   0.963380,
                        0.923897,   0.887088,   0.683552,   0.683180,
                        0.244258,   0.963484,   0.220534,   0.925960],
                       
                       [0.417075,  0.836787,  0.953429,  0.076610,
                        0.490397,  0.573417,  0.903105,  0.372850,
                        0.209912,  0.067709,  0.358607,  0.553040,
                        0.126210,  0.489527,  0.864474,  0.576415]]),

                ## sY = 
                array ([0.036805, 0.069215]),
                
                ## sPCG = 
                array([[0.7, 0.1], 
                       [0.3, 0.9]]),
                
                ## sLambdaPlus = 
                array([0.00277, 0.0008586])
                )
            }
    

    def test_feed_intermediate (self):
        (sLambdaMinus, sC, sY, sPCG, sLambdaPlus) = self.sample_data ()['i']
        n = Node ()
        
        for l in sLambdaMinus.iteritems ():
            n.feed (l[1], l[0])
            
        ## assert on _lambda_minus vector
        for l in sLambdaMinus.iteritems ():
            self.assertEqual (n._lambda_minus[l[0]].all (), l[1].all ())
        

    def test_inference_intermediate (self):
        (sLambdaMinus, sC, sY, sPCG, sLambdaPlus) = self.sample_data ()['i']
        n = Node ()
        n._C = sC
        n._PCG = sPCG
        
        for l in sLambdaMinus.iteritems ():
            n.feed (l[1], l[0])
            
        n.inference ()
        
        ## assert on y vector
        for i in range (len (n._y)):            
            self.assertTrue ( abs (n._y[i] - sY[i]) <= EPSILON )
            
        ## assert on lambda+ vector
        for i in range (len (sLambdaPlus)):
            self.assertTrue ( abs(n._lambda_plus[i] - sLambdaPlus[i]) <= EPSILON )


    def test_feed_entry (self):
        (sLambdaMinus, sC, sY, sPCG, sLambdaPLus) = self.sample_data ()['e']
        n = EntryNode ()
        
        n.feed (sLambdaMinus)
        self.assertEqual (n._lambda_minus.all (), sLambdaMinus.all ())

    def test_inference_entry (self):
        ## load sample data
        (sLambdaMinus, sC, sY, sPCG, sLambdaPLus) = self.sample_data ()['e']
        n = EntryNode ()
        n._C = sC
        n._PCG = sPCG
        
        n.feed (sLambdaMinus)
        n.inference ()

        for i in range (len (n._y)):
            self.assertTrue ( abs(n._y[i] - sY[i]) <= EPSILON )
##
##------------------------------------------------------------------------------
##  Main
##------------------------------------------------------------------------------
if __name__ == "__main__":
    unittest.main ()
