DISTANCE_THRESHOLD = 10 # ! FIXME this value does not make sense

##
## generate_training_seq (uInput :: array ) -> []
##
def generate_training_seq (uInput):
    return [(),]

##
## htm_train ( uNetwork :: Network
##             uTrainingSequence :: ( array, str ) )
##
def htm_train (uNetwork, uTrainingSequence):
    for current_layer in network.list_layers ():
        for (pattern, label) in uTrainingSequence:
            network.feed (pattern)

            for j in range (0, current_layer):
                layer = network.get_layer [j]

                for node in layer:
                    node.inference ()

            train ( (j, 
                     network.shared_mode_enabled_in (current_layer), 
                     current_layer ) )
            
    finalize_training (current_layer)

##
## train ( uLayer :: ( layer_label :: int,
##                     shared_mode_enabled :: Bool,
##                     nodes :: [n :: Node] )
##
def train (uLayer):
    global train_entry_node
    global train_intermediate_node
    (layer_label, shared_mode_enabled, nodes) = uLayer
    
    ## output level
    if len (nodes) == 1:
        [output_node] = nodes
        train_output_node (output_node)
    
    else:
        ## first level
        if layer_label == 0:
            training_procedure = train_entry_node
        ## intermediate levels
        else:
            training_procedure = train_intermediate_node
        
        training_procedure (nodes[0])

        if shared_mode_enabled:
            shared_state = nodes[0].clone_state ()
            for i in range (1, len(nodes)):
                nodes[i].set_state (shared_state)
                
        else:
            for i in range (1, len(nodes)):
                training_procedure (nodes[i])
            
            
def train_entry_nodes (uNode):
    s = uNode.clone_state ()
    lambda_minus = s['lambda_minus']
    seen_k_star = s['seen_k_star']
    coincidences = s['C']
    PCG = s['PCG']
    temporal_groups = s['temporal_groups']
    
    ## find the coincidence closest to lambda_minus
    ## that is, the *active* coincidence
    k_star = 0
    distance = linalg.norm ( coincidences[0] - lambda_minus.flatten ())
    
    for i in range (1, len (coincidences)):
        current_dist = linalg.norm ( coincidences[i] - lambda_minus.flatten ())
        if current_dist < distance:
            k_star = i
            distance = current_dist

    if distance > DISTANCE_THRESHOLD:
        ## make a new coincidence
        coincidences.concatenate (lambda_minus.flatten ())
        k_star = len (coincidences)
    
    if k_star == len (coincidences): seen_k_star[k_star] = 1
    else: seen_k_star[k_star] = seen_k_star[k_star] + 1
    
    ## !FIXME keep track of temporal gap
    if Input ().temporal_gap_active ():
        pass
        
    s.set_state ({ 'seen_k_star' : seen_k_star,
                   'latest_active_coinc' : k_star,
                   'C' : coincidences,
                   'PCG': PCG,
                   'temporal_groups' : temporal_groups })
                   

def train_intermediate_node (uNode):
    s = uNode.clone_state ()
    lambda_minus = s['lambda_minus']
    coincidences = s['C']
    PCG = s['PCG']
    temporal_groups = s['temporal_groups']
    
    
    
    

    

    
            
def train_output_node (uNode):
    pass
