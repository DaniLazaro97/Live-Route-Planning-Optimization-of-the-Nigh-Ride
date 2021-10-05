#Jon Ander Martin, Dani Lazaro, Almudena Chapa

#script use for plotting the routes obtained by the ACO
#A plot with numbered nodes is displayed:
    #Triangles represent pick-up locations.
    #Stop signs represent drop-off locations.
    #The vehicle (starting point) is represented with a diamond.

import matplotlib.pyplot as plt

def plot_route(customers, car_position, route):
       
    ## Extract initial and final points from customers
    initial_nodes = []  # [x,y]
    final_nodes = []   #[x,y]
    for customer in customers:
        initial_nodes.append(customer[0:2])
        final_nodes.append(customer[2:4])
        
    ## Create list with all nodes for route and rearrange
    if route != None:
        nodes = []
        nodes.extend(initial_nodes)
        nodes.extend(final_nodes)
        nodes.append(car_position)
        nodes_arranged = []
        for node_idx in route:
            nodes_arranged.append(nodes[node_idx])
        
        nodes_arranged_plot = [[],[]]
        for i in range(2*len(final_nodes)+1):
            nodes_arranged_plot[0].append(nodes_arranged[i][0])
            nodes_arranged_plot[1].append(nodes_arranged[i][1])
    
    fig, ax = plt.subplots()
        
    ## plot nodes
    plt.gca().set_prop_cycle(None)  # reset color cycle 
    for i in range(len(initial_nodes)):
        plt.scatter([initial_nodes[i][0]], [initial_nodes[i][1]],
                    marker='^',s=105)
        if route == None:
            plt.text(initial_nodes[i][0], initial_nodes[i][1], s=str(i))
    plt.gca().set_prop_cycle(None)  # reset color cycle 
    for i in range(len(final_nodes)):
        plt.scatter([final_nodes[i][0]], [final_nodes[i][1]],
                marker='8',s=105)
        if route == None:
            plt.text(final_nodes[i][0], final_nodes[i][1], s=str(i+5))
        
        
    ## plot car
    plt.scatter([car_position[0]], [car_position[1]],
                marker='d', s=105, c=0)
    
    ## plot route
    if route != None:
        plt.plot(nodes_arranged_plot[0], nodes_arranged_plot[1],
                 '--', c='chocolate', zorder=-5)
    
    plt.xlim([-10,10])
    plt.ylim([-10,10])
    plt.show()        
        
        
        
if __name__ == "__main__":
    customers=[[1,2,3,4,5],[6,7,8,9,0],[12,0,13,9,1]]
    route = [6,0,3,1,4,2,5]
    
    plot_route(customers, [5.5, -1], route)