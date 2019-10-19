import re


class Aircraft(object):
    def __init__(self, direction_from_airport=0):
        self.direction_from_airport = direction_from_airport


class Airport(object):
    def __init__(self, name="", icao="", iata="", runways=None, wind_speed=0, wind_direction=None):
        if runways is None:
            runways = []
        self.runways = runways
        self.name = name
        self.icao = icao
        self.iata = iata
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction

    # method to find best runway for aircraft
    def get_best_runway(self, aircraft: Aircraft):
        runway_names = []
        runway_distances = []

        if self.wind_speed > 5:
            reference_direction = self.wind_direction
            reverse_directions = False
        else:
            reference_direction = aircraft.direction_from_airport
            reverse_directions = True

        for runway in self.runways:
            # split runway to directions
            directions = runway.split("/")

            # parse runway data to degrees per direction
            # and calculate closest distances
            closest_dist_per_runway = []
            for direction in directions:
                distances = []
                # regex remove possible characters
                direction = re.sub("[A-Z]", "", direction)
                # add 3rd digit
                direction += "0"
                # convert to int
                direction = int(direction)
                # consider direction and reversed direction
                distances.append(abs(direction - reference_direction))
                distances.append(abs(direction - reference_direction + 360))
                distances.append(abs(direction - reference_direction - 360))
                # determine closest distance from both possible directions
                closest_distance = min(distances)
                closest_dist_per_runway.append(closest_distance)

            # save runway names based on wind conditions
            if reverse_directions:
                runway_names.append(directions[::-1])
            else:
                runway_names.append(directions)
            # save runway distances
            runway_distances.append(closest_dist_per_runway)

        # find nearest runway
        # determine closest runway distances
        closest_distances = []
        for distances in runway_distances:
            closest_distances.append(min(distances))
        # determine closest distance
        closest_distance = min(closest_distances)
        print(closest_distance)
        # match closest_distance with runway_distances
        for i in range(len(runway_distances)):
            if closest_distance in runway_distances[i]:
                nearest_runway = i
                nearest_runway_coord_index = runway_distances[i].index(closest_distance)
        # apply matched index on runway_names
        runway_name = runway_names[nearest_runway][nearest_runway_coord_index]

        return runway_name
