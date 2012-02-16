#!/usr/bin/python

from spatial_pooler import SpatialPooler

f = open ('data/characters', 'r')
lines = f.readlines ()
f.close ()

inputs = []

## read 5 chars
for i in range (5):
    input_vector = ""
    for j in range (10):
        if j == 0: continue ##discard the first line
        input_vector = input_vector + lines [(i*10) + j][1:]  
        
    input_vector = list (input_vector)
    
    ##filter some chars
    input_vector = [0 if item == ' ' or item == '\n' 
                    else item for item in input_vector]
    ##print input_vector
    inputs.append (input_vector)

# print len (inputs[1])
# print len (inputs[1][1])

sp = SpatialPooler ()
for i in inputs:
    print i
    sp.feed (i)
    print len (sp.quantization_centers ())
