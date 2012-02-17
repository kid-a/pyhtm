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
        self._lambda_minus = array ([]) ## input vector
        self._y = array ([])            ## density over coincidences
        self._lambda_plus = array ([])  ## output message
        
        ## state
        self._C = array ([[]])          ## coincidences matrix
        self._temporal_groups = set ([])## temporal groups
        self._PCG = array ([[]])        ## PCG matrix

        ## receptive field
        self.rf_begin = 0
        self.rf_end = 0

        ## name and links
        self.name = uName
        self.children = []
        self.parent = None
        

    def inference (self):
        self._y = self._lambda_minus * self._C
        self._lambda_plus = self._y * self._PCG


def Network (object):
    """The Network class. Contains nodes arranged in a hierarchy."""
    def __init__ (self, *args, **kwargs):
        self.layers = {}
        self.nodes = {}

    def feed (self, uInput, uTime = time.time()):
        ## transform the input into a flattened list
        flattened_input = [item for sublist in uInput for item in sublist]

        for node in self.layers[0]:
            node.feed (flattened_input [node.receptive_field_begin,
                                        node.receptive_field_end],
                       uTime)

    # ## let the '[]' operator on instances of this class
    # def __getitem__(self, attr):
    #     return self.__dict__[attr]
