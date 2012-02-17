"""
pyhtm.py
An implementation of Hierarchical Temporal Memory in Python.
"""

import time
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
    
    def feed (self, uLambda, uFrom):
        self._lambda_minus[uFrom] = uLambda

    def inference (self):
        ## compute density over coincidences
        for c in self._C:
            selected_features = []

            for (child,l) in self._lambda_minus.iteritems ():
                selected_features.append (l[c[child] - 1])

            self._y.append (reduce (mul, selected_features))

        ## compute density over temporal groups
        self._lambda_plus = dot( array (self._y), self._PCG)

    def propagate (self):
        parent.feed (self._lambda_plus, self.name)


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
