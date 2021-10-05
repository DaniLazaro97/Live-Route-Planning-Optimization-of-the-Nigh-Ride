#Jon Ander Martin, Dani Lazaro, Almudena Chapa

#This script contains the ACO algorithm (function name:ACO) and all the functions it needs.
#It is Dorigo's proposed algorithm. 
#It is call by the main_loop, where the needed parameters are specified in the lines 34-39.

import numpy as np
from random import random
from itertools import permutations

def calculate_distances(A,B):    
    dx = A[0] - B[0]
    dy = A[1] - B[1]
    dist = np.array([dx,dy])
    return np.linalg.norm(dist)


def create_nodes(customers,car_position,k):    
    nodes=[]  
    for i in range(2*k):       
        if i<k:
            node=[customers[i][0],customers[i][1]]
            nodes.append(node)
        else:
            node=[customers[i-k][2],customers[i-k][3]]
            nodes.append(node)
    nodes.append(car_position)
    return nodes


def ACO(k,customers,car_position,n_ants,alpha,beta,q0,ph_increment,evaporation_rate):
    
    customers=customers
    k=k
    alpha=alpha
    beta=beta
    car_position=car_position
    n_ants= n_ants      
    n_iterations=10
    evaporation_rate=evaporation_rate
    ph_increment= ph_increment
    q0=q0
    pheromone_matrix,distance_matrix,nodes=initialize_ACO(k,customers,car_position,ph_increment)
    waypoints=list(range(len(nodes)))
    length_best=100000
    for i in range(n_iterations):
        routes, pheromone_matrix=generate_route(waypoints,k,pheromone_matrix,distance_matrix,alpha,beta,evaporation_rate,ph_increment,n_ants,q0) 
        new_best_route,new_length_best= best_route_and_length(routes,distance_matrix)
        pheromone_matrix=daemon_update(pheromone_matrix,new_best_route,new_length_best,evaporation_rate)
        
        if new_length_best < length_best:
            length_best=new_length_best
            best_route=new_best_route
        
        route_nodes=order_nodes(best_route,nodes)
       
    return best_route,pheromone_matrix,distance_matrix,waypoints,route_nodes,length_best
   
        
def initialize_ACO(k,customers,car_position,ph_increment):    
    nodes=create_nodes(customers,car_position,k)
    distance_matrix=np.zeros((2*k+1,2*k+1))
    pheromone_matrix=ph_increment*np.ones_like(distance_matrix) #Initial value of pheromone in every path 
    for i in range (2*k+1):
        for j in range (2*k+1):
            distance_matrix[i,j]=calculate_distances(nodes[i],nodes[j])
            if i==j: #or j+k==i:
                pheromone_matrix[i,j]=0   #Paths going from destination to origin
                distance_matrix[i,j]=10**5
    return pheromone_matrix,distance_matrix,nodes
    
    
def generate_route (waypoints,k,pheromone_matrix,distance_matrix,alpha,beta,evaporation_rate,ph_increment,n_ants,q0):
    
    illegal= [waypoints[k:2*k] for i in range(n_ants)]
    position=[[waypoints[-1]] for i in range(n_ants)]
    routes=position
    
    
    for i in range(len(waypoints)-1): 
        arcs=[]               
        for j in range(n_ants):
            next_wpt= next_waypoint(routes[j],illegal[j],position[j][i],pheromone_matrix,distance_matrix,alpha,beta,q0)
            routes[j].append(next_wpt)            
            if next_wpt<k:
                illegal[j].remove(next_wpt+k) 
            arcs.append([position[j][i],next_wpt])
            position[j][i+1]=next_wpt
            
        #Once every ant takes an arc, pheromone is updated  
        increment_matrix=np.zeros_like(pheromone_matrix)
        pheromone_mat_copy=np.copy(pheromone_matrix)
        for arc in arcs:           
            increment=pheromone_update(pheromone_mat_copy[arc[0],arc[1]],evaporation_rate,ph_increment)
            increment_matrix[arc[0],arc[1]]+=increment
            pheromone_matrix[arc[0],arc[1]]=0
        pheromone_matrix+=increment_matrix           
    return routes, pheromone_matrix


def next_waypoint(route,illegal,position,pheromone_matrix,distance_matrix,alpha,beta,q0):
    pheromone=np.copy(pheromone_matrix[position])  #takes the row corresponding to the actual position
    pheromone[route]=0
    pheromone[illegal]=0
    attract_numerator=pheromone**alpha * (1/distance_matrix[position])**beta
    distance_matrix[position]
    attractiveness= attract_numerator/np.sum(attract_numerator)
    if random() <= q0:
        next_wpt = np.argmax(attractiveness)
    else:
        probabilities = attractiveness/ np.sum(attractiveness)
        next_wpt = np.random.choice(range(len(probabilities)),1, p=probabilities) 
    return int(next_wpt)

def pheromone_update(pheromone_arc,evaporation_rate,increment):
    pheromone_arc = (1-evaporation_rate)*pheromone_arc + evaporation_rate*increment
    return pheromone_arc

def best_route_and_length(routes,distance_matrix):
    all_lengths=[]
    for i in range(len(routes)):
        route_length=0
        for j in range (len(routes[0])-1):
            arc_length=distance_matrix[routes[i][j],routes[i][j+1]]
            route_length += arc_length
        all_lengths.append(route_length)
    best_route=np.argmin(all_lengths)
    
    return routes[best_route],all_lengths[best_route]

def daemon_update(pheromone_matrix,best_route,length_best,evaporation_rate):
    pheromone_matrix=(1-evaporation_rate)*pheromone_matrix
    for i in range (len(best_route)-1):
       pheromone_matrix[best_route[i],best_route[i+1]]+=evaporation_rate*1/length_best
    return pheromone_matrix

def order_nodes(route,nodes):
    route_nodes=[]
    for waypoint in route:
        route_nodes.append(nodes[waypoint])
    return route_nodes    

def route_length(route,distance_matrix):    
    route_length=0
    for i in range (len(route)-1):
        arc_length=distance_matrix[route[i],route[i+1]]
        route_length += arc_length
    return route_length                
       
def possible_routes(k):
    '''Generates all the combinations of nodes to create routes and filters the illegal routes'''
    #Not necessary in the ACO, but for making some tests
    perm = permutations(range(k*2))  
    per=[]
    
    for i in perm:  
        per.append((6,)+i)      
    all_permutations = np.array(per)   
    origin = [i for i in range(0,k)]
    dest = [i for i in range(k, 2*k)]
    zipped = zip(origin, dest)
    origin_dest_matrix = np.array(list(zipped))
    i = 0
    todelete = []
    for perm in all_permutations:
        for origindest  in origin_dest_matrix:
            if np.where(perm == origindest[0]) > np.where(perm == origindest[1]) :
                todelete.append(i)           
        i+=1    
    todelete = np.unique(todelete)
    all_permutations = np.delete(all_permutations, todelete, 0)
    
    return all_permutations


#%% TEST CODE
# if __name__ == "__main__":
#     customers=[[1,2,3,4,5],[6,7,8,9,0],[12,0,13,9,1]]
#     car_position=[2,1]
#     k=3
#     b,p,d,w,rn=ACO(k,customers,car_position,3,1,1)
    
    
#     all_routes=possible_routes(k)
#     all_lengths=[]
#     for route in all_routes:
#         length=route_length(route,d)
#         all_lengths.append(length)
#     idx=np.argmin(all_lengths) #No creo que vaya a haber dos rutas con la misma longitud y que sea justo la minima
#     print('Shortest route:', all_routes[idx]) 
#     print('Best found route:', b)