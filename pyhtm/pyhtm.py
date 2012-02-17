"""
pyhtm.py
An implementation of Hierarchical Temporal Memory in Python.
"""

import time
from numpy import *

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


def link (uChild, uParent):
    uChild.parent = uParent
    uParent.children.append (uChild)


class Node (object):
    def __init__ (self, uName = None, *args, **kwargs):
        """The Node class. """
        ## data
        ## self._incoming_messages = []
        self._lambda_minus = array ([]) ## input vector
        self._y = array ([])            ## density over coincidences
        self._lambda_plus = array ([])  ## output message
        
        ## state
        self._C = array ([[]])          ## coincidences matrix
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
        self._lambda_minus = array ([])
    
    def feed (self, uLambda):
        numpy.concatenate((self._lambda_minus, uLambda))

    def inference (self):
        self._y = self._lambda_minus * self._C
        self._lambda_plus = self._y * self._PCG

    def propagate (self):
        for child in self.children:
            child.feed (self._lambda_plus)
        self.clear_input ()




def Network (object):
    """The Network class. Contains nodes arranged in a hierarchy."""
    def __init__ (self, *args, **kwargs):
        self.layers = {}
        self.nodes = {}

    def feed (self, uInput, uTime = time.time()):
        for node in self.layers[0]:
            node.feed (uInput[node.starting_point['x']:uInput.delta['x'],
                              node.starting_point['y']:uInput.delta['y']])
