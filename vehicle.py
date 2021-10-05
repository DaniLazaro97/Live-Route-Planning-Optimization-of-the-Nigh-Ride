#Jon Ander Martin, Dani Lazaro, Almudena Chapa

#The class vehicle is defined:
    #ATRIBUTES:
        # position
        # current destination
        # current route: route already traveled
        # route: route assigned
    #METHODS:
        # move
        # update destination
        # update route
        
import numpy as np

class Vehicle(object):
    
    ## Vehicle parameters
    v = 0.87  # vehicle speed, we need to find a reasonable value
    
    def __init__(self):
        self.position = [0, 0]  # vector with vehicle position
        self.current_destination = [0, 0]
        self.current_route = []  # [[wpt1_x,wpt1_y], [wpt2_x,wpt2_y], ...]
        self.route=[]
                
    def move(self):
        """
        'move' moves the vehicle one step towards the current destination.

        Returns
        -------
        reached_destination_flag : BOOLEAN
            The flag will be True when the vehicle reaches the destination.
            Otherwise, it will be False.

        """
        destination = self.current_destination
        
        ## calculate direction
        dx = destination[0] - self.position[0]
        dy = destination[1] - self.position[1]
        dest_vector = np.array([dx,dy])
        dist = np.linalg.norm(dest_vector)  # distance to the next waypoint
        u = dest_vector / dist  # u is the unit direction vector
        
        ## avoid overshooting
        # if distance is larger than speed, advance a distance equal to speed
        # otherwise, reduce the speed to the distance
        if dist > self.v:
            vel = self.v * u
            reached_destination_flag = False
        else:
            vel = dist * u
            reached_destination_flag = True
            
        ## update position in x and y
        for i in [0,1]:
            self.position[i] = self.position[i] + vel[i]
            
        # check algorithm
        # print('New position: %r' % self.position)
        dest = np.array(destination)
        # print('New distance: %.5f' % np.linalg.norm(self.position - dest))
            
        return reached_destination_flag
            
    def update_destination(self):
        """
        update_destination sets a new current destination for the vehicle

        Returns
        -------
        end_of_route_flag : BOOLEAN
            Returns True if the end of the route is reached. Returns
            False if there are more destinations in the current route.

        """
        if self.current_route == []:
            end_of_route_flag = True
        else:
            self.current_destination = self.current_route.pop(0)
            end_of_route_flag = False
            # print('Destination reached. Moving to next waypoint: %r' % self.current_destination)
        return end_of_route_flag
    
    def update_route(self, new_route):
        """
        update_route sets a new route for the vehicle

        Parameters
        ----------
        new_route : LIST
            New route for the vehicle.
            The format must be
            [[waypoint1_x,waypoint1_y], [waypoint2_x,waypoint2_y], ...]
            
        """
        self.current_route = new_route
        self.update_destination()
        
        
        
    
if __name__ == "__main__":
    import numpy as np
    
    car = Vehicle()
    route = [[4,5], [3,1], [3,8]]
    car.update_route(route)
    route_flag = False
    
    while(1):
        flag = car.move()
        if flag:
            route_flag = car.update_destination()
        if route_flag:
            print('Route finished')
            break
    