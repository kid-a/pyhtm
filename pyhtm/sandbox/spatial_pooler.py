import math

D = 0.0 / 100.0

def compute_distance (uVector, uOther):
    """Compute the Euclidean distance between two vectors."""
    ## since each element can be either 0 or 1,
    ## no need for square roots and pow
    d = 0
    for i in range (len(uVector)):
        d = d + math.pow((int(uVector [i]) - int(uOther [i])), 2)

    return d

class SpatialPooler (object):
    def __init__ (self, *args, **kwargs):
        self.__quantization_patterns = []
        self.__distance = D

    def feed (self, uInputVector):
        distances = []
        for i in range (len (self.__quantization_patterns)):
            d = compute_distance (uInputVector, 
                                  self.__quantization_patterns[i])
            print d
            distances.append (d)
        
        almost_one_center_in_range = False
        for d in distances:
            if d < (self.__quantization_patterns * len (uInputVector)): 
                print "Center found!"
                almost_one_center_in_range = True ## what if more centers in range?

        ## if no quantization center found, 
        ## create a new one
        if not almost_one_center_in_range:
            self.__quantization_patterns.append (uInputVector)

    def quantization_centers (self): return self.__quantization_patterns
