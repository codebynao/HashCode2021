class Street:
    def __init__(self, name, intersections, time):
        self.name = name
        self.intersections = intersections
        self.time = time


class Car:
    def __init__(self, streets, index=0):
        self.streets = streets
        self.index = index
        self.time = 0
        self.end_time = 0


def print_result(crossed_intersections):
    file = open("output_d.txt", "w")
    file.write(str(len(crossed_intersections) - 1))
    for output_intersection in crossed_intersections[:-1]:
        file.write("\n" + str(output_intersection["index"]))
        file.write("\n" + str(output_intersection["nb_streets"]))
        for key in output_intersection.keys():
            if isinstance(output_intersection[key], dict):
                file.write("\n" + key + " " + str(output_intersection[key]["cycle_time"]))
    file.close()


def local_inputs():
    f = open("./inputs/d.txt", "r")
    input_data = f.read().splitlines()
    return input_data


def google_inputs():
    input_data = input().strip.split(' ')
    return input_data


def main():
    input_data = local_inputs()
    score = 0  # global score
    duration, intersections_number, streets_number, cars_number, bonus_points = [int(x) for x in input_data[0].split()]

    # Create all the streets
    streets = []
    for i in range(1, streets_number+1):
        input_data[i] = input_data[i].split()
        street = Street(input_data[i][2], (input_data[i][0], input_data[i][1]), int(input_data[i][3]))
        streets.append(street)

    # Create all the cars
    cars = []
    for i in range(streets_number+1, streets_number+cars_number+1):
        input_data[i] = input_data[i].split()
        car = Car(input_data[i][1:])
        cars.append(car)
        car.index = len(cars) - 1

    elapsed_time = 0
    crossed_intersections = []
    # We are going to remove cars that arrived at their final destination to avoid looping through them again
    filtered_cars = cars[::-1]
    global_cars_arrived_indexes = []
    while elapsed_time < duration:
        # Copy the filtered cars, we're going to loop through this list
        loop_cars = filtered_cars.copy()
        elapsed_time += 1
        print(elapsed_time)
        cars_arrived_indexes = []
        for i in range(len(loop_cars)):
            # If the car does not have any more street to go to, it means that it arrived at its final destination
            if len(loop_cars[i].streets) == 0 and loop_cars[i].time <= 0:
                # We add its index to the list of cars indexes to remove for the next loop
                cars_arrived_indexes.insert(0, i)
                global_cars_arrived_indexes.append(loop_cars[i].index)
                # Keep the end time of the car to be able to add bonus points because it arrived before the end of the simulation
                loop_cars[i].end_time = elapsed_time
                continue

            # If the car time is to 0, it means that it reached an intersection, decisions need to be made
            if loop_cars[i].time == 0:
                # Get the next street to go
                car_street = loop_cars[i].streets.pop(0)
                for street in streets:
                    if street.name == car_street:
                        car_street = street
                        break

                # Handle the current intersection traffic
                intersection = None
                for c_i in crossed_intersections:
                    if car_street.intersections[1] == c_i["index"]:
                        intersection = c_i
                # If we never crossed this intersection before, we can directly pass the street light to green (True)
                if intersection == None:
                    crossed_intersections.append({
                        "index": car_street.intersections[1],
                        "nb_streets": 1,
                        car_street.name: {
                            "light": True,
                            "cycle_time": 0,
                            "scheduled": False
                        }
                    })
                # If we already crossed this intersection, it means that some traffic lights have already been scheduled
                else:
                    # We pass the street light to green (True)
                    if car_street.name in intersection:
                        if not intersection[car_street.name]["light"]:
                            intersection[car_street.name]["light"] = True
                    else:
                        intersection["nb_streets"] += 1
                        intersection[car_street.name] = {
                            "light": True,
                            "cycle_time": 0,
                            "scheduled": False
                        }
                    # Let's pass all the other lights of the intersection to red (False)
                    for key in intersection.keys():
                        if isinstance(intersection[key], dict) and key != car_street.name:
                            intersection[key]["light"] = False
                            intersection[key]["scheduled"] = True

                # Update the car time to the street time (time it will take the car to reached the end of the street)
                loop_cars[i].time = car_street.time
            # Make the car advance by decrementing the car time
            loop_cars[i].time -= 1

        # Let's increment the intersections light cycles
        for crossed_intersection in crossed_intersections:
            for key in crossed_intersection.keys():
                if isinstance(crossed_intersection[key], dict) and ((crossed_intersection[key]["light"] and not crossed_intersection[key]["scheduled"]) or crossed_intersection[key]["cycle_time"] == 0):
                    crossed_intersection[key]["cycle_time"] += 1

                    # Remove all the cars that arrived at their final destination, no need to loop through them again
        for car_index in cars_arrived_indexes:
            filtered_cars.pop(car_index)

    # Increment the score with the cars that arrived at their final destination
    for index in global_cars_arrived_indexes:
        if len(cars[index].streets) == 0:
            score += bonus_points
            score = score + (duration - cars[index].end_time)

    # If some cars arrived at the last second, they won't be in global_cars_arrived_indexes, so let's find them
    for car in filtered_cars:
        if len(car.streets) == 0:
            score += bonus_points
            score = score + (duration - car.end_time)

    print(score)

    print_result(crossed_intersections)

    # Print Output
    # print(len(crossed_intersections))
    # for output_intersection in crossed_intersections[:-1]:
    #     print(output_intersection["index"])
    #     print(output_intersection["nb_streets"])
    #     for key in output_intersection.keys():
    #         if isinstance(output_intersection[key], dict):
    #             print(key, output_intersection[key]["cycle_time"])


if __name__ == '__main__':
    main()
