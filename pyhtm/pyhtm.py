"""
pyhtm.py
An implementation of Hierarchical Temporal Memory in Python.
"""

import time
from numpy import *
from operator import mul


class Clock (object):
    """The Clock. Implements the Borg Pattern."""
    __shared_state = {}
    
    def __init__ (self, *args, **kwargs):
        self.__dict__ = self.__shared_state
        self.__time = 0 ## initialized to zero
        self.__delta = 0 ## actual value of delta !FIXME for future purposes
        
    def step (self): self.__time = self.__time + 1
    def now (self): return self.__time
    def reset (self): self.__time = 0


class Node (object):
    def __init__ (self, uName = None, *args, **kwargs):
        """The Node class. """
        ## data
        self._lambda_minus = {}         ## input_vector
        self._y = []                    ## density over coincidences
        self._lambda_plus = array ([])  ## output message
        
        ## state
        self._C = []                    ## coincidences
        self._temporal_groups = set ([])## temporal groups
        self._PCG = array ([[]])        ## PCG matrix

        ## receptive field
        self.starting_point = {}
        self.delta = {}

        ## name and links
        self.name = uName
        self.children = []
        self.parent = None

    def clear_input (self):
        self._lambda_minus = []
    
    def feed (self, uLambda, uFrom):
        self._lambda_minus[uFrom] = uLambda

    def inference (self):
        ## compute density over coincidences
        for c in self._C:
            selected_features = []

            for (child,l) in self._lambda_minus.iteritems ():
                selected_features.append (l[c[child] - 1])

            self._y.append (reduce (mul, selected_features))

        ## compute density over temporal groups
        print self._y
        self._lambda_plus = dot( array (self._y), self._PCG)

    def propagate (self):
        parent.feed (self._lambda_plus, self.name)


class Network (object):
    """The Network class. Contains nodes arranged in a hierarchy."""
    def __init__ (self, *args, **kwargs):
        self.layers = {}
        self.nodes = {}

    def feed (self, uInput, uTime = time.time()):
        for node in self.layers[0]:
            node.feed (uInput[node.starting_point['x']:uInput.delta['x'],
                              node.starting_point['y']:uInput.delta['y']],
                       'input')
            
            
def link (uChild, uParent):
    uChild.parent = uParent
    uParent.children.append (uChild)
                
class NetworkBuilder (object):
    """A NetworkBuilder class. Implements methods to build complex networks."""
    def __init__ (self, *args, **kwargs):
        pass
