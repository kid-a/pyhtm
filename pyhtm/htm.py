#!/usr/bin/python

TIME = 0 # clock
        
class Region:
    def __init__ (self, uSize, uInputsNumber, *args, **kwargs):
        self._columns = []
        self._synapses_map = {}
        m = uSize[0]
        n = uSize[1]

        ## prepare the synapses map
        for i in range (uInputsNumber):
            self._synapses_map[i] = []
        
        ## create a matrix of m x n columns
        ## attach a number of synapses to each column
        ## !FIXME a synapse factory would be useful here
        for i in range (m):
            self._columns.append ([])

            for j in range (n):
                new_column = Column ( (i, j) )

                ## create a potential synapse for each input bit
                ## and attach it to the column
                for k in range (uInputsNumber):
                    new_synapse = Synapse ()
                    self._synapses_map[k].append (new_synapse)
                    new_column._potential_synapses.append (new_column)
                    
                self._columns[i].append (new_column)

        self._columns_collection = [c for sublist in self._columns for c in sublist]

        self._min_overlap = 2             # minimum number of active inputs
        self._desired_local_activity = 3  # number of winning columns
        ##self._overlap

        self._boost = 1
        self._inhibition_radius = 1
        self._overlap_vector = {}
        self._active_columns = []
        self._current_input =  [0 for i in range (uInputsNumber)] ## pretty unuseful


    def neighbours (self, uColumn, uRadius = None):
        """ return the list of columns within inhibition radius from uColumn """
        # print uRadius
        if uRadius is None: uRadius = self._inhibition_radius
        x = uColumn._name [0]
        y = uColumn._name [1]
        # print x, y
        neighbours_l = []

        if uRadius == 1:
            for i in range (x - 1, x + 2):
                for j in range (y - 1, y + 2):
                    ## try to get the (i-th, j-th) element
                    ## if the element doesn't exist (i.e. we are on the edge of the matrix)
                    ## just continue
                    ##print i, j
                    try: 
                        if i == x and j == y: raise ## remove same element
                        if i < 0 or j < 0: raise ## needed, since c[-1][-1] makes sense in python
                        neighbours_l.append ( self._columns[i][j] )
                    except: continue
                    
            return neighbours_l

        else: ## uRadius > 1
            ## pick all the immediate neighbours, i.e. uRadius = 1
            immediate_neighbours = self.neighbours (uColumn, 1)
            neighbours_l1 = immediate_neighbours
            
            ##then, expand your selection
            for column in immediate_neighbours:
                neighbours_l1 = self.neighbours (column, uRadius - 1)
                neighbours_l.extend (neighbours_l1)

            ## remove duplicates
            s = set (neighbours_l)
            s.remove (uColumn)
            return list (s)

    def kth_score (self, uColumns, k):
        #print uColumns
        ##print list (self._overlap_vector)
        uOverlapVector = dict ( [(c, v) for (c, v) in self._overlap_vector.iteritems () 
                                 if c in uColumns] )
        ##uOverlapVector = dict ( [c for c in list (self._overlap_vector) if c in uColumns] )
        # print uOverlapVector
        o = sorted (uOverlapVector.iteritems (), key = lambda pair : pair[1]) ## sort by overlap value
        return o[k - 1]


    def overlap (self):
        """Given an input vector, calculates the overlap of each column with that vector. """
        overlap_v = []
        
        for c in self._columns_collection:
            overlap = 0
            for s in c._connected_synapses:
                overlap = overlap + s._input
                
            if overlap < self._min_overlap: overlap = 0
            else: overlap = overlap * c._boost
        
            overlap_v.append ( (c, overlap) )
            
        self._overlap_vector = dict (overlap_v)


    def inhibite (self):
        self._active_columns = []
        
        for c in self._columns_collection:
            try: min_local_activity = self.kth_score (self.neighbours (c), 
                                                      self._desired_local_activity)
            except: 
                print "desired local activity too high. exiting."
                exit (-1)
        
            if self._overlap_vector[c] > 0 and \
               self._overlap_vector >= min_local_activity:
               
                self._active_columns.append (c)
        

    def spatial_pooler (self):
        self.overlap ()
        self.inhibite ()
        ## learn (self._columns)
        ## ! FIXME -> we need to model time here
        ## ! FIXME -> we need to model inhibition radius and neigbourood relationships
        ## ! FIXME -> overlap_vector, active_columns, etc. can be made instance-related data

    def feed (self, uInputVector):
        """Feed the synapses and invoke the spatial pooler """
        for i in range (len (uInputVector)):
            input_bit = uInputVector[i]
            for synapse in self._synapses_map[i]:
                synapse._input = input_bit

        ## now, invoke the spatial pooler
        self.spatial_pooler ()


class Column:
    def __init__ (self, uName, *args, **kwargs):
        self._name = uName ## it is a tuple
        self._potential_synapses = []
        self._connected_synapses = [] ## !FIXME maybe some synapses are connected at first, randomly
        self._cells = None


# class Cell:
#     def __init__ (self, *args, **kwargs):
#         pass


class Synapse:
    def __init__ (self, *args, **kwargs):
        self._input = None ## 0 | 1
        self._weigth = 0

if __name__ == "__main__":
    print "HTM prototype starting..."
    ##r = Region ( (10, 5) )
    r = Region ( (5, 5), uInputsNumber=25 )

    # print r._columns
    # column = r._columns [1][2]
    # print column._name

    # neighbours = r.neighbours (column)
    # neighbours = sorted(neighbours, key = lambda c : c._name[0])
    # for n in neighbours:
    #     print n._name
    # print len (neighbours)

    i = [0, 1, 0, 1, 0,
         0, 1, 0, 1, 0,
         0, 1, 0, 1, 0,
         0, 1, 0, 1, 0,
         0, 1, 0, 1, 0]

    print r._active_columns
    r.feed (i)
    r.feed (i)
    r.feed (i)
    r.feed (i)
    print r._active_columns

    ##for s in r._synapses
