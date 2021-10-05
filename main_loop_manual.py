#Jon Ander Martin, Dani Lazaro, Almudena Chapa

#This script is used for getting the humand by hand routes.
#The random seed in line 26 must be the same as the seed in line 36 in the main_loop.
#When run, the user will be asked to complete several routes.
#A plot with numbered nodes is displayed for each new case:
    #Triangles represent pick-up locations.
    #Stop signs represent drop-off locations.
    #The vehicle (starting point) is represented with a diamond.
#User has to introduce manually the sequence of nodes that make the route, each number separated by a blank space
#Finally, the program outputs:
    #Mean waiting time of customers
    #Total distances traveled by each car
    #Customers served by each car
    
import numpy as np
import matplotlib.pyplot as plt
import random
from vehicle import Vehicle
from classifier import get_customers
from ACO_function import ACO, route_length, initialize_ACO, order_nodes
from plot_routes import plot_routes
from obtain_figures import plot_route

## PARAMETERS
simulation_time = 400     # time-steps for the simulation
customer_freq = 8         # simulation time-steps of interval between customer appearances
k = 5                      # customers to pick from pool
n_initial_customers = 20   # customers at t=0

## ACO PARAMETERS
ACO_alpha = 1
ACO_beta = 6
ACO_ants = 20

random.seed(97)

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

def get_user_route():
    error_flag = True
    while error_flag:
        raw_input_string = input('Answer: ')
        ls = raw_input_string.split()
        for i in range(len(ls)):
            ls[i] = int(ls[i])
            
        # Check if length is correct
        error_flag = False
        if len(ls) != 10:
            error_flag = True
            print('Error! The length of the list is incorrect.')
            continue
        
        # Check for illegal routes
        len_half = int(len(ls)/2)
        for j in range(len_half):
            dif = ls.index(j+len_half) - ls.index(j)
            if dif < 0:
                error_flag = True
                print('Error! Illegal route.')
                break
    return ls


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
        plot_route(customers, vehicle.position, None)  # give the user the points
        best_route = get_user_route()  # the user chooses the route
        best_route.insert(0,len(best_route))  # add the vehicle as the first stop in the route
        _,distance_matrix,nodes = initialize_ACO(k, customers, vehicle.position.copy(),1/65)
        route_dist = route_length(best_route, distance_matrix)
        # best_route,_,_,_,nodes,route_length = ACO(k,customers,vehicle.position.copy(),ACO_ants,ACO_alpha,ACO_beta)
        total_distance[i] += route_dist
        plot_route(customers, vehicle.position, best_route)
        
        nodes = order_nodes(best_route, nodes)
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
                customers, customer_pool = get_customers(vehicle.position, customer_pool, k)
                customers_list.append(customers)
                mean_t += add_waiting_time(customers)
                mean_t_samples += 5
                customers_picked[i] += 5
                # best_route,pheromone_matrix,distance_matrix,waypoints,route_nodes
                print('Iteration %d/%d' % (t, simulation_time))
                plot_route(customers, vehicle.position, None)  # give the user the points
                best_route = get_user_route()  # the user chooses the route
                best_route.insert(0,len(best_route))  # add the vehicle as the first stop in the route
                _,distance_matrix,nodes = initialize_ACO(k, customers, vehicle.position.copy(),1/65)
                route_dist = route_length(best_route, distance_matrix)
                # best_route,_,_,_,nodes,route_length = ACO(k,customers,vehicle.position.copy(),ACO_ants,ACO_alpha,ACO_beta)
                total_distance[i] += route_dist
                plot_route(customers, vehicle.position, best_route)
                
                nodes = order_nodes(best_route, nodes)
                vehicle.route=nodes.copy()
                nodes.pop(0)  # remove the current vehicle position
                vehicle.update_route(nodes)
                vehicles[i] = vehicle
                
                
                # print('Vehicle %d end of route. Updating...' % i)
                # customers, customer_pool = get_customers(vehicle.position, customer_pool, k)
                # mean_t += add_waiting_time(customers)
                # mean_t_samples += 3
                # # get new customers and route and update
                # best_route,_,_,_,nodes,route_length = ACO(k,customers,vehicle.position.copy(),ACO_ants,ACO_alpha,ACO_beta)
                # total_distance[i] += route_length
                # #plot_route(customers, vehicle.position, best_route)
                # vehicle.route=nodes.copy()
                # nodes.pop(0)  # remove the current vehicle position
                # vehicle.update_route(nodes)
            
            vehicles[i] = vehicle
                
        # if t<=120:
        #     if t%2==0:
        #         plot_routes(vehicles,t,customer_pool)
        # increase waiting time of customers in pool
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
            