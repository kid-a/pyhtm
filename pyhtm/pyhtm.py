"""
pyhtm.py
An implementation of Hierarchical Temporal Memory in Python.
"""

import time
import math
from numpy import *
from operator import mul
import yaml


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
        """The Node class. """
        ## data
        self._lambda_minus = {}         ## input_vector
        self._y = []                    ## density over coincidences
        self._lambda_plus = array ([])  ## output message
        
        ## state
        self._C = []                    ## coincidences
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
        self._lambda_minus = []

    def compute_density_over_coinc (self):
        for c in self._C:
            selected_features = []

            for (child,l) in self._lambda_minus.iteritems ():
                selected_features.append (l[c[child] - 1])

            ## compute each element of y as the multiplication
            ## of the selected features
            self._y.append (reduce (mul, selected_features))

    def compute_density_over_groups (self):
        self._lambda_plus = dot( array (self._y), self._PCG)        

    def compute_class_posterior_probabilities (self):
        pass
    
    def feed (self, uLambda, uFrom):
        self._lambda_minus[uFrom] = uLambda

        
    def inference (self):
        """Inference is a template method."""
        compute_density_over_coinc ()
        compute_density_over_groups ()
        compute_class_posterior_probabilities ()


    def propagate (self):
        parent.feed (self._lambda_plus, self.name)


class EntryNode (Node):
    """The EntryNode class. Implements the peculiar input manipulation
    and inference mechanism of a node beloning to the entry level of 
    a network.""" 
    def __init__ (self, uSigma = 1, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)

        self._lambda_minus = array ([[]]) ## small input patch
        self._sigma = uSigma
        
    def feed (self, uInput):
        """For entry level nodes, the input is a plain numpy array."""
        self._lambda_minus = uInput

    def compute_density_over_coinc (self):
        """For entry level nodes, the y vector is obtained comparing 
        the coincidence with the input message, by means of the euclidean
        norm."""
        for c in self._C:
            ## compute the euclidean norm with Frobenius formula
            norm = linalg.norm (c - self._lambda_minus)
            distance = math.exp ( - math.pow (norm / float (self._sigma), 2))
            self._y.append (distance)


class OutputNode (Node):
    """The OutputNode class. Implements the peculiar inference mechanism of 
    the outer level nodes."""
    def __init__ (self, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)
        
        ## state
        ## !FIXME what about cleaning up??
        self._prior_class_prob = array ([]) ## prior class probabilities
        self._PCW = array ([[]])            ## PCW matrix
        self._densities_over_classes = array ([]) 
        self._class_posterior_prob = array ([])
        
    def compute_density_over_groups (self):
        self._densities_over_classes = dot( array (self._y), self._PCW)

    def compute_class_posterior_probabilities (self):
        total_probability = 0
        for k in range (len (self._densities_over_classes)):
            total_probability = total_probability + \
                ( self._densities_over_classes [k] * self._prior_class_prob [k] )

        for j in range (len (self._densities_over_classes)):
            self._class_posterior_prob [j] = self._densities_over_classes * \
                self._prior_class_prob / float (total_probability)

        self._lambda_plus = self._class_posterior_prob
            

class Network (object):
    """The Network class. Contains nodes arranged in a hierarchy."""
    def __init__ (self, uName = None, *args, **kwargs):
        self.name = uName
        self.layers = {}
        self.nodes = {}

    def feed (self, uInput, uTime = time.time()):
        for node in self.layers[0]:
            node.feed (uInput[node.starting_point['x']:uInput.delta['x'],
                              node.starting_point['y']:uInput.delta['y']],
                       'input')
            
            
def link (uChild, uParent):
    uChild.parent = uParent
    uParent.children.append (uChild)
                

class NetworkBuilder (object):
    """A NetworkBuilder class. Implements methods to build complex networks."""
    def load (self, uFile):
        f = open (uFile)
        content = f.read ()
        f.close ()

        net_descr = yaml.load (content)
        network = Network (uName = net_descr['name'])
        
        for layer in net_descr['layers']:
            [nodes] = layer.values ()
            [layer_name] = layer.keys ()

            list_of_nodes = []
            for node_name in nodes:
                n = Node(uName = node_name)
                list_of_nodes.append (n)
                network.nodes[node_name] = n
            
            network.layers[layer_name] = list_of_nodes

        for node in net_descr['nodes']:
            [node_name] = node.keys()
            for (attribute_name, attribute_value) in node[node_name].iteritems():
                if attribute_name == 'coincidences' and \
                        attribute_value != 'undefined':
                    network.nodes[node_name]._C = attribute_value

                if attribute_name == 'PCG' and \
                        attribute_value != 'undefined':
                    network.nodes[node_name]._PCG = attribute_value

                if attribute_name == 'temporal_groups' and \
                        attribute_value != 'undefined':
                    network.nodes[node_name]._temporal_groups = attribute_value

                if attribute_name == 'children' and \
                        attribute_value != 'undefined':
                    network.nodes[node_name].children = attribute_value

        return network

    def save (self, uFile, uNetwork):
        n = uNetwork
        d = dict ()
        d['name'] = n.name
        d['nodes'] = []
        d['layers'] = []


        for (layer_name, list_of_nodes) in n.layers.iteritems ():
            l = [node.name for node in list_of_nodes]
            d['layers'].append ({layer_name : l})
            
        for (node_name, node_instance) in n.nodes.iteritems ():
            node = {node_name : dict ()}

            if node_instance._C != []: 
                node[node_name]['coincidences'] = node_instance._C

            if node_instance._PCG != array ([]): 
                node[node_name]['PCG'] = node_instance._PCG.tolist ()

            if node_instance._temporal_groups != set ([]): 
                node[node_name]['temporal_groups'] = \
                    node_instance._temporal_groups.tolist ()

            node[node_name]['children'] = \
                [child for child in node_instance.children]

            d['nodes'].append (node)

        f = open(uFile, 'w')
        f.write (yaml.dump (d))
        f.close ()
