#!/usr/bin/python
from numpy import array as array

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def load_amat (uFilePath, uWidth = 0):
    f = open (uFilePath, 'r')
    content = f.readlines ()
    f.close ()

    accumulator = []
    if uWidth == 0:
        for line in content:
            row = map (lambda x : float (x), line.split ())
            accumulator.append (row)

        return array (accumulator)

    else:
        for line in content:
            #print len(line)
            subsample = []
            for chunk in chunks (line.split (), uWidth):
                row = map (lambda x : float (x), chunk)
                if len (row) == 1: 
                    [label] = row
                    subsample = (label, array (subsample))
                    break
                subsample.append (array (chunk) )
    
            accumulator.append (subsample)
        
        return accumulator


def test():
    l = load_amat ('/home/loris/Downloads/rectangles_train.amat', 28)
    print l

if __name__ == "__main__":
    test ()
    
    
    
    
        
