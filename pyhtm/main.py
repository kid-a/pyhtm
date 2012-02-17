from pyhtm import *

if __name__ == "__main__":
    builder = NetworkBuilder ()
    network = builder.load ('priv/myfirstnetwork.yaml')
    builder.save ('priv/myfirstnetwork-generated.yaml', network)
    
    
    
    
    
