"""
pyhtm.py
An implementation of Hierarchical Temporal Memory in Python.
"""

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
    

class Node (object):
    def __init__ (self, uName = None, *args, **kwargs):
        self._input_vector = {} ## an empty dict
        self._PCG = array ([[]]) ## an empty matrix
        self._coincidences = array ([[]]) ## an empty vector of vectors
        self._temporal_groups = set ([])
        self._name = uName

    def feed_input (self, uChild, uLambda):
        self._input_vector[uChild] = uLambda
        
