#!/usr/bin/python

TIME = 0 # a ticking clock


class Region (object):
    """Implements an HTM region."""
    def __init__ (self, uSize, uInputsNumber, *args, **kwargs):
        ## Internal data:
        self._columns = []        ## columns
        self._active_columns = [] ## current active columns
        self._input_vector = []   ## input vector
        
        ## Some params, now:
        ## Number of desired winning columns 
        self._DESIRED_LOCAL_ACTIVITY = (10 / 100.0) * len (self._columns) 

        ## column inhibition radius
        self._INHIBITION_RADIUS = 1

        ## Minimum number of active synapses for a column
        ## to be taken into account during inhibition
        self._MIN_OVERLAP = 1                  
        
        ## Synapse permanence increase and decrease steps
        self._PERMANENCE_INC = 0.10
        self._PERMANENCE_DEC = 0.10

    ## let the '[]' operator on instances of this class
    def __getitem__(self, attr):
        return self.__dict__[attr]

    @classmethod
    def kth_score (uColumns, k):
        pass

    @classmethod
    def max_duty_cycle (uColumns):
        pass

    def average_receptive_field_size (self):
        pass

    def overlap (self):
        pass

    def inhibite (self):
        pass
    
    def learn (self):
        pass


class Column (object):
    """Model a column of cells."""
    def __init__ (self, *args, **kwargs):
        pass

    ## let the '[]' operator on instances of this class
    def __getitem__(self, attr):
        return self.__dict__[attr]



class Synapse (object):
    """Model an HTM synapse."""

    ## Permanence threshold upon which the synapse
    ## is considered connected
    connected_permanence = 0.5 

    def __init__ (self, *args, **kwargs):
        ## Internal data:        
        self._permanence = 0   ## bounded between 0 and 1
        self._input_bit = None ## the input bit

    ## let the '[]' operator on instances of this class
    def __getitem__(self, attr):
        return self.__dict__[attr]
    

if __name__ == "__main__":
    print "HTM prototype starting..."
    r = Region ( (5, 5), 25 )
