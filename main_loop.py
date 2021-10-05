#Jon Ander Martin, Dani Lazaro, Almudena Chapa

#Simulation environment for the live route planning algorithm for UC's NightRide

#Parameters of the environment are described in lines 28-31
#Parameters used in the ACO algorithm are described in lines 34-39

#The program outputs:
    #Mean waiting time of customers
    #Total distances traveled by each car
    #Customers served by each car

import numpy as np
import matplotlib.pyplot as plt
import random
from vehicle import Vehicle
from classifier import get_customers
from ACO_function import ACO
from plot_routes import plot_routes
from obtain_figures import plot_route
#from first_five import get_customers            #for FIFO criterion to be used in the selection of customers
                                                 #Deactivate line 17 if used
time=[]
length=[]

for i in range(1):             # This loop was used with 300 runs for the comparison (clustering VS FIFO) 
    ## PARAMETERS
    simulation_time = 400      # time-steps for the simulation
    customer_freq = 8          # simulation time-steps of interval between customer appearances
    k = 5                      # customers to pick from pool
    n_initial_customers = 20   # customers at t=0
    
    ## ACO PARAMETERS
    ACO_alpha = 1              # controls the type of choice heuristic 
    ACO_beta = 6               # controls the type of choice heuristic 
    ACO_ants = 20              # number of ants
    q0=0.2                     # probability of greedy choice
    ph_increment=1/65          # fixed pheromone increment over an arc every time an ant takes the arc
    evaporation_rate=0.2       # evaporation rate
    
    random.seed(97)
    
    routes=[]
    def create_customer():
        new_customer = []
        ## add 4 random parameters for initial and final X and Y position
        for parameter in range(4):
            new_customer.append(random.uniform(-10,10))
        new_customer.append(0)  # set the waiting time
        return new_customer
    
    def add_waiting_time(customers):
        delta = 0
        for customer in customers:
            delta += customer.pop(-1)
        return delta
    
    if __name__ == "__main__":
        ###################  INITIALIZATION  ###################
        ## create vehicles
        vehicle1 = Vehicle()
        vehicle2 = Vehicle()
        vehicles = list([vehicle1, vehicle2])
        
        ## create initial pool of customers
        customer_pool = []
        for i in range(n_initial_customers):  
            customer_pool.append(create_customer())
        customer_pool_global = list(customer_pool)
        
        ## Set initial routes for vehicles
        total_distance = [0,0]
        customers_list=[]
        for i in [0,1]:
            vehicle = vehicles[i]
            customers, customer_pool = get_customers(vehicle.position, customer_pool, k)
            customers_list.append(customers)
            # best_route,pheromone_matrix,distance_matrix,waypoints,route_nodes
            best_route,_,_,_,nodes,route_length = ACO(k,customers,vehicle.position.copy(),ACO_ants,ACO_alpha,ACO_beta,q0,ph_increment,evaporation_rate)
            routes.append(route_length)
            total_distance[i] += route_length
            # plot_route(customers, vehicle.position, best_route)
            # plot_route(customers, vehicle.position, None)
            # print(best_route)
            vehicle.route=nodes.copy()
            nodes.pop(0)  # remove the current vehicle position
            vehicle.update_route(nodes)
            vehicles[i] = vehicle
            
        ## initialize metrics
        mean_t = 0
        mean_t_samples = 10
        customers_picked = [5,5]
            
        
        ###################  MAIN LOOP  ###################
        xx = []
        customer_pool_size = []
        for t in list(range(simulation_time)):
            
            ## add new random customer every customer_freq timesteps
            if t % customer_freq == 0:
                cust = create_customer()
                customer_pool.append(cust)
                customer_pool_global.append(cust)
            
            ## update vehicles
            for i in [0,1]:
                vehicle = vehicles[i]
                
                ## 1. move
                waypoint_flag = vehicle.move()
                
                ## If waypoint reached, change destination
                list_flag = False
                if waypoint_flag:
                    list_flag = vehicle.update_destination()
                
                ## If end of current customer list, find new customers
                if list_flag:
                    # get customers
                    # print('Vehicle %d end of route. Updating...' % i)
                    customers, customer_pool = get_customers(vehicle.position, customer_pool, k)
                    customers_list.append(customers)
                    customers_picked[i] += 5
                    mean_t += add_waiting_time(customers)
                    mean_t_samples += 5
                    # get new customers and route and update
                    best_route,_,_,_,nodes,route_length = ACO(k,customers,vehicle.position.copy(),ACO_ants,ACO_alpha,ACO_beta,q0,ph_increment,evaporation_rate)
                    routes.append(route_length)
                    total_distance[i] += route_length
                    #plot_route(customers, vehicle.position, best_route)
                    vehicle.route=nodes.copy()
                    nodes.pop(0)  # remove the current vehicle position
                    vehicle.update_route(nodes)
                
                vehicles[i] = vehicle
                    
            # if t<=120:
            #     if t%2==0:
            #         plot_routes(vehicles,t,customer_pool)
            #increase waiting time of customers in pool
            for i in range(len(customer_pool)):
                customer_pool[i][-1] += 1
                
            if t % 10 == 0:
                xx.append(t)
                customer_pool_size.append(len(customer_pool))
                pass
            
        # fig, ax = plt.subplots()
        # plt.plot(xx, customer_pool_size)
        
        print('Mean waiting time: %.2f u' % (mean_t*1.0/mean_t_samples))
        print('Total distance traveled by the vehicles: %r' % total_distance)
        print('Customers picked by vehicles: %r' % customers_picked)
        #print('Mean best route length:', sum(routes)/len(routes))     
        # time.append(mean_t*1.0/mean_t_samples)
        # length.append(sum(routes)/len(routes))
# mean_time=sum(time)/len(time)
# mean_length= sum(length)/len(length)     
# print('Mean waiting time:', mean_time)
# print('Mean best route length:',mean_length)
# variance_t = sum([((x - mean_time) ** 2) for x in time]) / len(time)
# res_t = variance_t ** 0.5
# variance_l = sum([((x - mean_length) ** 2) for x in length]) / len(length)
# res_l = variance_l ** 0.5
# print('Mean std time:', res_t)
# print('Mean best route std:',res_l)