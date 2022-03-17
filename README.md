# Road trip !:

Here, we were provided with the following :

* road-segments.txt - a dataset of major highway segments of the United States (and parts of southern Canada and 
northern Mexico), including highway names, distances, and speed limits.

* city-gps.txt - a dataset of cities and towns with corresponding latitude-longitude positions.

* route.py - it contained the skeleton code where we are supposed to publish our solution.

## Problem Statement

To complete the get_route() function, which returns the best route according to the specified cost function, as well as 
the number of segments, number of miles, number of hours for a car driver, and expected number of hours for the delivery
driver.

##Solution

The solution comprises the implementation of the code route.py. The problem was addressed with the A* search algorithm.
A* algorithm is a form of Best First Search algorithm which computes the cost using the following formula :

f(s) = g(s)+h(s)

where g(s) is the cost of the best path found so far to s and h(s) is an admissible heuristic which never overestimates 
the cost.


## Abstractions

Based upon the problem given, these are the following abstractions:

State Space - It is the collection of all cities/nodes which are available in the driver's universe. All the nodes for
which the coordinates (latitude and longitude) are provided to us, can be considered as the state space in this problem.

Initial State - The initial-city or the starting city in this problem is our initial state

Goal State - It is the final state or in this case the final destination city where the driver is supposed to reach from
the initial state.

Successor Function - Successor Function is nothing but a function which provides the user with the next successive 
states. In this case, if we are providing an input city to the successor function, then the adjacent cities connected 
to our input are the successors. This can be computed by logically traversing the road-segments.txt file. 

Cost Function - The cost function f(s) consists of two parts, g(s) and h(s). g(s) is the optimal cost (distance covered,
time taken, segments traversed, and delivery time taken) computed from the source state to the next successive state 
(computed with successor function). h(s) is estimated admissible cost computed that provides us with the best result.

## Design Decisions

A number of data structures including list, tuple, dictionary, heapq etc. and a variety of inbuilt functions like 
math.sqrt, math.tanh, sorted were used in this solution. The main approach followed here is to compute the successors or
successive cities of our source node and this is implemented using a dictionary. From that dictionary, the most optimal 
successor is selected and this optimality is decided using the cost function provided by the user. This cost function 
can be distance travelled, the shortest time, delivery time or segments traversed. The heapq is used to maintain the 
fringe and pop out the suitable and most optimal successor based on the priority. 

## Difficulties

Several problems were encountered while designing the optimal solution to the given problem. These are mentioned below : 

* Initially the solution was implemented using the priority queue, but it was observed that it was taking a lot of time 
to compute the solution. Later on, it was implemented using the heapq which is nothing but a heap implementation of a 
priority queue. The main advantage with heapq is that is provides us with the smallest element in the least amount of 
time which was O(log(n)).

* It was difficult to compute a cost function for the calculation of segments.

