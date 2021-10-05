Main\_loop.py 

- Run this file to simulate the whole environment. 
- Simulation environment for the live route planning algorithm for UC's NightRide. 
- A 20×20 bi-dimensional space where customers are located, and vehicles can move. In each step, the vehicles move a fixed distance *v* towards the next way-point in their current  route.  If  they  reach  a  way-point,  they  pick-up  or  drop-off a  customer  and proceed to the next way-point.  If the way-point they reach is the end of their current route, they execute the customer allocation.  
- Routes are generated using an ACO algorithm. 
- Parameters of the environment are described in lines 28-31. 
- Parameters used in the ACO algorithm are described in lines 34-39. 
- The program outputs: 
- Mean waiting time of customers. 
- Total distances traveled by each vehicle. 
- Customers served by each vehicle. 

Main\_loop\_manual.py 

- Run this file to manually try to set the routes (with customer list provided by allocation algorithm). 
- The random seed in line 26 must be the same as the seed in line 36 in the main\_loop.py  to compare results. 
- When run, the user will be asked to complete several routes. For every new route: 
- A plot with numbered nodes is displayed. 
  - Triangles represent pick-up locations. 
  - Stop signs represent drop-off locations. 
  - Same color points represent one customer (pick-up and drop-off). 
  - The vehicle (starting point) is represented with a black diamond. 
- The user must introduce manually the sequence of nodes that make the route, each number separated by a space. For example, if the route designed is 0-1-2- 3-4-5, the user must write ‘0 1 2 3 4 5’ (without the quotes). 

▪  2 errors can happen: a drop-off node is scheduled in the route before the pick-up location, or there are nodes missing or repeated. In either case, an error message will appear and the user will be asked to input the route again. 

- The program outputs: 
- Mean waiting time of customers. 
- Total distances traveled by each car. 
- Customers served by each car. 
