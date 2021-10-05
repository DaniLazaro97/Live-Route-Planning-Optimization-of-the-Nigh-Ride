#Jon Ander Martin, Dani Lazaro, Almudena Chapa

#script use for selecting the 5 first customers in the pool when the FIFO criterion is used

import numpy as np

def get_customers(vehicle_position, customer_list, k):

    selected_customers = []
    for i in range(k):
        selected_customers.append(customer_list[i])
    
    ## customer pool without the selected customers
    new_pool = list(customer_list)

    del new_pool[0:k]
            
    return selected_customers, new_pool
            
    