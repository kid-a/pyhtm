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


def make_node (uType, uName, uSigma = 1):
    if   uType == 'e': return Node (uName, EntryNodeBehaviour (uSigma))
    elif uType == 'i': return Node (uName, IntermediateNodeBehaviour ())
    elif uType == 'o': return Node (uName, OutputNodeBehaviour ())


class Node (object):
    def __init__ (self, uName, uBehaviour, *args, **kwargs):
        """The Node class. """
        ## name and links
        self.name = uName               ## the node's name
        self.children = []              ## the node's children
        self.parent = None              ## the node's parent

        ## behaviour
        self._behaviour = uBehaviour    ## Entry, Intermediate or Output node

        ## receptive field
        self.starting_point = {}        ## the starting point of the RF
        self.delta = {}                 ## extension of the RF in xy coordinates

    def clone_state (self): return self._behaviour.clone_state ()
    def set_state (self, uState): self._behaviour.set_state (uState)

    def feed (self, uInput, uFrom): 
        self._behaviour.feed (uInput, uFrom)
                
    def inference (self):
        self._behaviour.inference ()

    def propagate (self):
        self._behaviour.propagate (self.name, self.parent)



class EntryNodeBehaviour (object):
    def __init__ (self, uSigma = 1, *args, **kwargs):
        ## data
        self._lambda_minus = array([]) ## input vector
        self._sigma = uSigma           ## speed of deviation of each y[i]
        self._y = []                   ## density over coincidences
        self._lambda_plus = array ([]) ## output message

        ## state
        self._C = []
        self._temporal_groups = set ([]) 
        self._PCG = array ([[]])

    ##
    ## clone_state () -> { ('C' | 'PCG' | 'temporal_groups') : value }
    ##
    def clone_state (self):
        return { 'C'               : self._C,
                 'PCG'             : self._PGC,
                 'temporal_groups' : self._temporal_groups }

    ##
    ## set_state ( uState :: { ('C' | 'PCG' | 'temporal_groups') : value } )
    ##
    def set_state (self, uState):
        self._C = uState['C']
        self._PCG = uState['PCG']
        self._temporal_groups = uState ['temporal_groups']
        
    def feed (self, uInput, _uFrom):
        self._lambda_minus = uInput

    def inference (self):
        self.compute_density_over_coinc ()
        self.compute_density_over_groups ()

    def compute_density_over_coinc (self):
        """For entry level nodes, the y vector is obtained comparing 
        the coincidence with the input message, by means of the euclidean
        norm."""
        for c in self._C:
            ## compute the euclidean norm with Frobenius formula
            norm = linalg.norm (c - self._lambda_minus.flatten ())
            distance = math.exp ( - math.pow (norm / float (self._sigma), 2))
            self._y.append (distance)

    def compute_density_over_groups (self):
        self._lambda_plus = dot( array (self._y), self._PCG)

    def propagate (self, uMyName, uParent):
        uParent.feed (self._lambda_plus, uMyName)        

    
class IntermediateNodeBehaviour (object):
    def __init__ (self, *args, **kwargs):
        ## data
        self._lambda_minus = {}        ## input dict
        self._y = []                   ## density over coincidences
        self._lambda_plus = array ([]) ## output message
        
        ## state
        self._C = []
        self._temporal_groups = set ([]) 
        self._PCG = array ([[]])

    ##
    ## clone_state () -> { ('C' | 'PCG' | 'temporal_groups') : value }
    ##
    def clone_state (self):
        return { 'C'               : self._C,
                 'PCG'             : self._PGC,
                 'temporal_groups' : self._temporal_groups }

    ##
    ## set_state ( uState :: { ('C' | 'PCG' | 'temporal_groups') : value } )
    ##
    def set_state (self, uState):
        self._C = uState['C']
        self._PCG = uState['PCG']
        self._temporal_groups = uState ['temporal_groups']

    def feed (self, uLambda, uFrom):
        self._lambda_minus[uFrom] = uLambda

    def inference (self):
        self.compute_density_over_coinc ()
        self.compute_density_over_groups ()

    def compute_density_over_coinc (self):
        for c in self._C:
            selected_features = []

            for (child,l) in self._lambda_minus.iteritems ():
                selected_features.append (l[c[child] - 1])
            
            self._y.append (reduce (mul, selected_features))
            
    def compute_density_over_groups (self):
        self._lambda_plus = dot( array (self._y), self._PCG)

    def propagate (self, uMyName, uParent):
        uParent.feed (self._lambda_plus, uMyName)


class OutputNodeBehaviour (object):
    def __init__ (self, *args, **kwargs):
        ## data
        self._lambda_minus = {}        ## input dict
        self._y = []                   ## density over coincidences
        self._lambda_plus = array ([]) ## output message
        
        ## state
        self._C = []
        self._prior_class_prov = array ([])       ## prior class probabilities
        self._PCW = array ([])                    ## PCW matrix
        self._densities_over_classes = array ([]) ## densities over classes
        self._class_posterior_prob = array ([])   ## class posterior probabilities

    def feed (self, uLambda, uFrom):
        self._lambda_minus[uFrom] = uLambda

    def inference (self):
        self.compute_density_over_coinc ()
        self.compute_density_over_classes ()
        self.compute_class_posterior_probabilities ()

    def compute_density_over_coinc (self):
        for c in self._C:
            selected_features = []

            for (child,l) in self._lambda_minus.iteritems ():
                selected_features.append (l[c[child] - 1])
            
            self._y.append (reduce (mul, selected_features))

    def compute_density_over_classes (self):
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

    def propagate (self, uMyName, uParent):
        pass
            

class Network (object):
    """The Network class. Contains nodes arranged in a hierarchy."""

    ##
    ##__init__ ( uName :: str )
    ##
    def __init__ (self, uName = None, *args, **kwargs):
        self.name = uName               ## :: str
        self.layers = {}                ## :: {int : [n :: Node,],}
        self.nodes = {}                 ## :: {str : [n :: Node,],}
        self.shared_mode_levels = set() ## :: set ( int )

    ##
    ## list_layers () -> [l :: int]
    ##
    def list_layers (self):
        return [l for l in self.layers.iterkeys ()]

    ##
    ## get_layer ( uLayerName :: int ) -> [n :: Node]
    ##
    def get_layer (self, uLayerName):
        """ Returns a list containing a reference to all nodes in the 
        layer identified  by uLayerName """
        return self.layers[uLayerName]

    ##
    ## enable_shared_mode ( uLayerName :: int )
    ##
    def enable_shared_mode (self, uLayerName):
        self.shared_mode_levels.add (uLayerName)
        
    ##
    ## disable_shared_mode ( uLayerName :: int )
    ##
    def disable_shared_mode (self, uLayerName):
        try: self.shared_mode_levels.remove (uLayerName)
        except: raise Exception ("Shared mode was not enabled for layer " + 
                                 str(uLayerName))

    ##
    ## shared_mode_enabled_in ( uLayerName :: int )
    ##
    def shared_mode_enabled_in (self, uLayerName):
        if uLayerName in self.shared_mode_levels: return True
        else: return False

    ##
    ## feed ( uInput :: numpy.array,
    ##        uTime  :: time.time )       
    ## !FIXME node feed is not working yet
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
                ## create entry level nodes for level zero:
                if int(layer_name) == 0:
                    n = make_node ('e', node_name)
                ## create output nodes for the output level:
                elif (int(layer_name) + 1) == len (net_descr['layers']):
                    n = make_node ('o', node_name)
                ## else, create an intermediate node:
                else:
                    n = make_node ('i', node_name)
                list_of_nodes.append (n)
                network.nodes[node_name] = n
            
            network.layers[layer_name] = list_of_nodes

        for node in net_descr['nodes']:
            [node_name] = node.keys()
            for (attribute_name, attribute_value) in node[node_name].iteritems():
                if attribute_name == 'coincidences' and \
                        attribute_value != 'undefined':
                    network.nodes[node_name].behaviour._C = attribute_value

                if attribute_name == 'PCG' and \
                        attribute_value != 'undefined':
                    network.nodes[node_name].behaviour._PCG = attribute_value

                if attribute_name == 'temporal_groups' and \
                        attribute_value != 'undefined':
                    network.nodes[node_name].behaviour._temporal_groups = attribute_value

                if attribute_name == 'children' and \
                        attribute_value != 'undefined':
                    ## set children
                    network.nodes[node_name].children = attribute_value
                    
                    ## set the 'parent' attribute in children
                    for child in network.nodes[node_name].children:
                        network.nodes[child].parent = network.nodes[node_name]

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

            if node_instance._behaviour._C != []: 
                node[node_name]['coincidences'] = node_instance._C

            # if node_instance._behaviour._PCG != array ([]): 
            #     node[node_name]['PCG'] = node_instance._PCG.tolist ()

            # if node_instance._behaviour._temporal_groups != set ([]): 
            #     node[node_name]['temporal_groups'] = \
            #         node_instance._temporal_groups.tolist ()
                
            node[node_name]['children'] = \
                [child for child in node_instance.children]

            d['nodes'].append (node)

        f = open(uFile, 'w')
        f.write (yaml.dump (d))
        f.close ()
