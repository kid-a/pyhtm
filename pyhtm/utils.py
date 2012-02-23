from numpy import array as array

def load_amat (uFilePath):
    f = open (uFilePath, 'r')
    content = f.readlines ()
    f.close ()

    accumulator = []
    for line in content:
        row = map (lambda x : float (x), line.split ())
        accumulator.append (row)
        
    return array (accumulator)
    
    
        
