#Jon Ander Martin, Dani Lazaro, Almudena Chapa

#script use for plotting the routes and customer pool for making the simulation time-lapse
    #Customers in the pool are represented with grey dots
    #Vehicle position is represented with an X and its allocated customers and traveled route is...
       #...represented in the same color (red/blue)

import matplotlib.pyplot as plt


def plot_routes(vehicles,t,customer_pool): 
    
    for cust in customer_pool:
        plt.scatter(cust[0], cust[1],color='gray')
        plt.scatter(cust[2], cust[3],color='gray')
    for (i,c) in zip([0,1],['b','r']):
            
        j=1
        for coord in vehicles[i].route:       
                plt.scatter(coord[0], coord[1],color=c) 
                plt.scatter(vehicles[i].position[0],vehicles[i].position[1], marker='x',color=c,s=200)
                plt.text(coord[0]+0.2, coord[1], '{}'.format(j))
                j+=1
         
        missing=len(vehicles[i].current_route)+1 #current route doesn't consider current_destination
        completed=vehicles[i].route[0:len(vehicles[i].route)-missing]+[vehicles[i].position]

        x=[]
        y=[]
    
        for pos in completed:

            x.append(pos[0])
            y.append(pos[1])
        plt.plot(x,y,c=c)
    plt.title('t={}'.format(t)) 
    plt.xlim([-10,10])
    plt.ylim([-10,10])
    #plt.savefig(f'routes/{t}.png', dpi = 1000)
    plt.show()  