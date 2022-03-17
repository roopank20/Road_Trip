#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: Sri Varsha Chellapilla (srchell), Roopank Kohli (rookohli) and Akash Bhapkar (abhapkar)
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#
# !/usr/bin/env python3

import sys
import math
import heapq


# Method to calculate the Euclidean distance between two cities.
def euclidean_distance(coordinates_for_city_1, coordinates_for_city_2):
    x1, y1 = coordinates_for_city_1
    x2, y2 = coordinates_for_city_2

    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


# Method to fetch and return the connected cities from the source city.
# A dictionary has been created "road_database" and is structured in such a manner that it provides the connected cities
# from the source city
def successors(city, road_database):
    return road_database[city].keys()


# Method to check if distance can be calculated between two cities. If yes, then computation of distance between
# both the cities is done.
def distance_between_cities(city_one, city_two, gps_database, calculated_distance_between_cities):
    # If coordinates for any of the cities is not available, then euclidean_distance between the cities will be zero
    if city_one not in gps_database.keys() or city_two not in gps_database.keys():
        return 0
    city_pair = tuple(sorted((city_one, city_two)))

    return calculated_distance_between_cities.get(city_pair, euclidean_distance(gps_database[city_one],
                                                                                gps_database[city_two]))


# Based on the cost function passed. this method returns the value of the heuristic among the cities present in the
# fringe. This value helps to sort the fringe elements and next element is based on the value returned.
def get_priority_index(cost_function, end_city, present_state_of_search, gps_database,
                       calculated_distance_between_cities):

    route_so_far, distance_so_far, segments_so_far, time_elapsed_so_far, delivery_time_so_far = present_state_of_search
    current_city = route_so_far[-1]
    # speed limit is taken to be the highest speed in the road-segments.txt file. This is done to ensure that our
    # heuristic is admissible and returns the optimal value.
    speed_limit = 65

    if cost_function == "segments":
        segments_covered = 1
        return segments_so_far + segments_covered

    if cost_function == "distance":
        distance_to_cover = distance_between_cities(current_city, end_city, gps_database,
                                                    calculated_distance_between_cities)
        return distance_so_far + distance_to_cover

    if cost_function == "time":
        distance_to_cover = distance_between_cities(current_city, end_city, gps_database,
                                                    calculated_distance_between_cities)
        distance_to_cover += distance_so_far
        if len(present_state_of_search[0]) == 1:
            time_required_to_destination = 0
        else:
            time_required_to_destination = (distance_to_cover / speed_limit)
        return time_elapsed_so_far + time_required_to_destination

    if cost_function == "delivery":
        distance_to_cover = distance_between_cities(current_city, end_city, gps_database,
                                                    calculated_distance_between_cities)
        distance_to_cover += distance_so_far

        if speed_limit < 50:
            if len(present_state_of_search[0]) == 1:
                delivery_time_to_destination = 0
            else:
                delivery_time_to_destination = distance_to_cover / speed_limit
            return delivery_time_so_far + delivery_time_to_destination
        else:
            if len(present_state_of_search[0]) == 1:
                delivery_time_to_destination = 0
                delivery_time_so_far += delivery_time_to_destination
            else:
                delivery_time_to_destination = distance_to_cover / speed_limit

                delivery_time_so_far += delivery_time_to_destination + (
                        2 * (delivery_time_to_destination + delivery_time_so_far) * math.tanh(distance_to_cover / 1000))
            return delivery_time_so_far


# Method to read the file "road-segments.txt". It returns a dictionary which contains every row of the file.
def read_segments_data(file):
    road_database = {}
    with open(file, 'r') as f:
        for line in f.readlines():
            segments = line.split()
            city_one = segments[0]
            city_two = segments[1]
            miles = segments[2]

            if not road_database.get(city_one, None):
                road_database[city_one] = {}
            if not road_database.get(city_two, None):
                road_database[city_two] = {}

            road_database[city_one][city_two] = (float(miles), float(segments[3]), segments[4])
            road_database[city_two][city_one] = (float(miles), float(segments[3]), segments[4])
    return road_database


# Method to read the file "city-gps.txt". It returns a dictionary which has the coordinates for each and every city
# present in this file.
def read_gps_data(file):
    gps_database = {}
    with open(file, 'r') as f:
        for line in f.readlines():
            file_data = line.split()
            gps_database[file_data[0]] = (float(file_data[1]), float(file_data[2]))
    return gps_database

# Method to create and initialize fringe before the code starts computation from the source city. Here, the sorting is
# being done using heapq, which stores the data in the form of a heap.
def initializeFringe(start_city, end_city, cost_function, gps_database,
                     calculated_distance_between_cities):
    fringe, route_so_far = [], [start_city]
    segments_so_far, distance_so_far, time_elapsed_so_far, delivery_time_so_far = 0, 0, 0, 0
    initial_fringe_element = (route_so_far, distance_so_far, segments_so_far, time_elapsed_so_far, delivery_time_so_far)
    priority_index = get_priority_index(cost_function, end_city, initial_fringe_element, gps_database,
                                        calculated_distance_between_cities)
    heapq.heappush(fringe, (priority_index, initial_fringe_element))
    return fringe


def get_route(start_city, end_city, cost_function):
    road_database = read_segments_data("road-segments.txt")
    gps_database = read_gps_data("city-gps.txt")
    if end_city not in gps_database:
        exit()

    calculated_distance_between_cities = {}
    visited = {}
    priority_index_when_visited = {}
    visited_List = []
    fringe = initializeFringe(start_city, end_city, cost_function, gps_database,
                              calculated_distance_between_cities)

    while fringe:
        #pop out the next city from the fringe based on priority
        priority_index, (route_so_far, distance_so_far, segments_so_far, time_elapsed_so_far, delivery_time_so_far) = \
            heapq.heappop(fringe)
        source = route_so_far[-1]
        if source == end_city:
            route_taken = [
                (route_so_far[index + 1], "{} for {} miles".format(road_database[route][route_so_far[index + 1]][2],
                                                                   road_database[route][route_so_far[index + 1]][0]))
                for index, route in enumerate(route_so_far[:-1])]

            result = {"total-segments": len(route_taken), "total-miles": distance_so_far,
                      "total-hours": time_elapsed_so_far, "total-delivery-hours": delivery_time_so_far,
                      "route-taken": route_taken}
            return result

        # Mark the city as visited and note down the priority
        visited[source] = True
        priority_index_when_visited[source] = priority_index

        # Generate successors
        next_cities = successors(source, road_database)
        for city in next_cities:
            if city in visited_List:
                continue
            else:
                miles_to_city, speed_limit, _ = road_database[source][city]
                time_to_city = miles_to_city / speed_limit
                # segments_covered = miles_to_city / 24.24

                segments_covered = 1

                if speed_limit < 50:
                    delivery_time_to_city = miles_to_city / speed_limit
                else:
                    delivery_time_to_city = time_to_city + (
                            2 * (time_to_city + delivery_time_so_far) * math.tanh(
                        miles_to_city / 1000))

                next_fringe_element = (
                route_so_far + [city], distance_so_far + miles_to_city, segments_so_far + segments_covered,
                time_elapsed_so_far + time_to_city, delivery_time_so_far + delivery_time_to_city)
                priority_index = get_priority_index(cost_function, end_city, next_fringe_element, gps_database,
                                                    calculated_distance_between_cities)

                has_city_been_visited = visited.get(city, False)

                if has_city_been_visited and priority_index < priority_index_when_visited[
                    city] and cost_function != "segments":
                    visited[city] = False
                    heapq.heappush(fringe, (priority_index, next_fringe_element))
                if not has_city_been_visited:
                    heapq.heappush(fringe, (priority_index, next_fringe_element))

    """
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time 
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """

    # route_taken = [("Martinsville,_Indiana","IN_37 for 19 miles"),
    #                ("Jct_I-465_&_IN_37_S,_Indiana","IN_37 for 25 miles"),
    #                ("Indianapolis,_Indiana","IN_37 for 7 miles")]
    #
    # return {"total-segments" : len(route_taken),
    #         "total-miles" : 51.,
    #         "total-hours" : 1.07949,
    #         "total-delivery-hours" : 1.1364,
    #         "route-taken" : route_taken}

    return None


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise (Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise (Exception("Error: invalid cost function"))
    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])
