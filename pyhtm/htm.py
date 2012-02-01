#!/usr/bin/python

import copy

TIME = 0 # a ticking clock


class Region (object):
    """Implements an HTM region."""
    def __init__ (self, uSize, uInputsNumber, *args, **kwargs):
        ## Internal data:
        self._columns = []        ## columns
        self._active_columns = [] ## current active columns
        self._input_vector = []   ## input vector
        self._synapses = {}       ## synapses map: <input-bit, list-of-synapses>
        
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

        ## Let's prepare the synapses map:
        for i in range (uInputsNumber):
            self._synapses [i] = []

        ## Now, let's create the columns
        ## they will be arranged in a m x n matrix
        ## also, attach one synapse per input bit
        ## to each column
        m = uSize[0]
        n = uSize[1]

        for i in range (m):
            self._columns.append ([])

            for j in range (n):
                c = Column ( (i, j) )
                self._columns[i].append (c)
                
                for k in range (uInputsNumber):
                    s = Synapse ()
                    c._potential_synapses.append (s)
                    self._synapses[k].append (s)


    ## let the '[]' operator on instances of this class
    def __getitem__(self, attr):
        return self.__dict__[attr]


    def compute_neighbours (self, uColumn, uRadius = None):
        """Return the list of columns within _INHIBITION_RADIUS from uColumn """
        if uRadius is None: uRadius = self._INHIBITION_RADIUS        
        neighbours = set ()

        ## stop condition:
        if uRadius == 1:
            ## get the column coordinates
            x = uColumn._coordinates[0]
            y = uColumn._coordinates[1]

            for i in range (x - 1, x + 2):
                for j in range (y -1, y + 2):
                    ## try to get the (i-th, j-th) element
                    ## if the element doesn't exist 
                    ## (i.e. we are on the edge of the matrix)
                    ## just go ahead
                    try:
                        if i == x and j == y: raise
                        if i < 0 or j < 0: raise
                        neighbours.add (self._columns[i][j])
                    except: continue

            return list (neighbours)
        
        ## recursive clause, i.e. uRadius > 1
        else:
            ## get the immediate neighbours, i.e.
            ## those such that |uColumn - neighbours| = 1
            immediate_neighbours = set (self.compute_neighbours (uColumn, 1))
            
            ## then, expand the selection area:
            for column in immediate_neighbours:
                for neighbour in self.compute_neighbours (column, uRadius - 1):
                    neighbours.add (neighbour)

            ## last, add the immediate neighbours
            neighbours = neighbours.union (immediate_neighbours)
            return list (neighbours)


    @staticmethod
    def kth_score (uColumns, k):
        """ Given a number of columns, retrieve the k-th highest overlap
        value among them."""
        overlap_vector = {}
        for c in uColumns: overlap_vector [c['_coordinates']] = c['_overlap']
        sorted_vector = sorted (overlap_vector.iteritems (),
                                key = lambda pair : pair [1]) [::-1]
        
        return sorted_vector[k - 1]


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
    def __init__ (self, uCoordinates, *args, **kwargs):
        ## Internal data:
        ## The column coordinates (x, y)
        self._coordinates = uCoordinates

        ## SP Overlap of this column with the current input
        self._overlap = 0

        ## List of columns within the current inhbition radius
        self._neighbours = []

        ## Boost factor for this column
        ## as computed during the learning phase
        self._boost = 0

        ## List of potential synapses
        self._potential_synapses = []

        ## List of connected synapses
        self._connected_synapses = []

        ## Active Duty Cycle, i.e. a sliding average representing 
        ## how often this column has been active after inhibition
        ## e.g. during the last 1000 iterations
        self._active_duty_cycle = 0

        ## Overlap Duty Cycle, i.e. a sliding average representing
        ## how oftern this column has had overlap with the input greater 
        ## than the region's minimum overlap 
        self._overlap_duty_cycle = 0

        ## Minimum Duty Cycle, i.e. how often this column should 
        ## be active. This value to be calculated as 1% of the maximum 
        ## firing rate of its neighbours
        self._MINIMUM_DUTY_CYCLE = 0 ## !FIXME read above


    ## let the '[]' operator on instances of this class
    def __getitem__ (self, attr):
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
    print r._columns[2][3]
    n = r.compute_neighbours (r._columns[2][3], uRadius = 1)
    print len (n)
    for neighbour in n:
        print neighbour._coordinates, neighbour

    a = r._columns[2][3]
    b = r._columns[3][3]
    c = r._columns[4][4]

    a._overlap = 2
    b._overlap = 3
    c._overlap = 4

    l = [a,b,c,]
    
    print Region.kth_score (l, 2)
    print Region.kth_score (l, 1)
    print Region.kth_score (l, 3)
        
    
