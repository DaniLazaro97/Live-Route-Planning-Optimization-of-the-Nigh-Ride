#Jon Ander Martin, Dani Lazaro, Almudena Chapa

#Clustering algorithm for customer allocation
#The vehicles are the centers of the clusters 
#Setting waiting time of the vehicle to the highest one of the customers in the pool...
  #... gives more weight to the ones that have been in queue the longest
import numpy as np

def get_customers(vehicle_position, customer_list, k):
    """
    get_customers selects the k customers closer to a vehicle from the
    customer pool

    Parameters
    ----------
    vehicle_position : LIST
        [x,y] position of the vehicle.
    customer_list : LIST
        [customer_1, customer_2, ...].
    k : INT
        Number of customers to pick from customer_list.

    Returns
    -------
    selected_customers : LIST
        List with selected customers' vectors.
    new_pool : LIST
        list of customers from customer_list that have not been selected by
        get_customers.

    """
    
    ## find customer with maximum waiting time
    max_time = 0
    for customer in customer_list:
        time = customer[-1]
        if time > max_time:
            max_time = time
    
    ## define vehicle's vector
    vehicle = []
    vehicle.extend(vehicle_position)
    vehicle.extend(vehicle_position)
    vehicle.append(max_time)
    
    ## calculate distances from vehicle to each customer
    distances = []
    vehicle_np = np.array(vehicle)
    for customer in customer_list:
        customer_np = np.array(customer)
        distances.append(np.linalg.norm(vehicle_np - customer_np))
    
    idx = np.argsort(distances)
    idx = idx[0:k]
    
    ## list with customers
    selected_customers = []
    for i in range(k):
        selected_customers.append(customer_list[idx[i]])
    
    ## customer pool without the selected customers
    new_pool = list(customer_list)
    for j in sorted(idx, reverse=True):
        del new_pool[j]
            
    return selected_customers, new_pool
    
    
    
    
if __name__ == "__main__":
        
    customer_pool = [[3,4,5,6,0],
                     [1,2,7,8,3],
                     [-1,1,5,5,4],
                     [-5,-4,3,3,3],
                     [0,0,9,9,8],
                     [1,-5,5,-1,7]]
    
    get_customers([1,2], customer_pool, 3)