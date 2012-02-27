from pyhtm import *

if __name__ == "__main__":
    # entry_node = make_node ('e', 'first')
    # intermediate_node = make_node ('i', 'second')
    # output_node = make_node ('o', 'third')



    builder = NetworkBuilder ()
    network = builder.load ('priv/myfirstnetwork.yaml')
    # for n in network.nodes.itervalues ():
    #     print n.children 
    #     print n.parent
    ##builder.save ('priv/myfirstnetwork-generated.yaml', network)
    
    # for n in network.nodes.iteritems():
    #     print n
    
    
    
    
