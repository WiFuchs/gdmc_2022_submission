import csv
from abc import ABC, abstractmethod
import math
import numpy as np
from typing import TYPE_CHECKING, List, Tuple
from BuildingSpecifications import Building

if TYPE_CHECKING:
    from village_planner import BuildArea


class BuildingEncyclopedia:
    """ BuildingEncyclopedia represents the interest functions between all buildings and the terrain.
        It is used by each BuildingType to calculate the interest value of building a building at a particular location.
    """
    def __init__(self, attraction_file):
        self.attract_repulse = {}
        with open(attraction_file, mode='r', encoding='utf-8-sig') as attr:
            reader = csv.DictReader(attr)
            for line in reader:
                self.attract_repulse[line["house_type"]] = {k: list(map(int, v.split(','))) for k, v in line.items() if
                                                            k != "house_type"}
        # TODO extend this with other weights / interest functions / etc


class BuildingType:
    def __init__(self, name, radius):
        self.name = name
        self.radius = radius
        self.structure = None
        self.orientation = None

    def calc_interest(self, build_area: 'BuildArea', point, building_locations: List[Building],
                      encyclopedia: BuildingEncyclopedia) -> float:
        """Calculate the interest of building at this point based on location and the world state
            :returns
                float in the range 0-1
        """
        # TODO figure out how to weight this
        # assert self.weights.sum() == 1.0  # Weights must be normalized

        # calculate inter-building attraction
        interest = self._attract_repulse(encyclopedia, building_locations, point[0], point[1])
        if interest == -1:
            return 0

        # interest = np.multiply(interest_vals, self.weights).sum()
        assert interest <= 1.0
        return interest

    def _attract_repulse(self, encyclopedia: BuildingEncyclopedia, building_locations: List[Building], x, z):
        """Lennard-Jones Potential function that repels at close distances and attracts at larger distances.
            Break_even is the distance where the function switches from repelling to attracting
        """
        if not building_locations:
            return 0.5

        interest = 0
        # loop over all buildings and calculate interest from them
        for building in building_locations:
            min_dist, max_dist, break_even = encyclopedia.attract_repulse[self.name][building.building_type.name]
            d = math.dist((building.x, building.z), (x, z))
            # if the distance to any house is out of bounds, this is not a suitable building location
            if d < min_dist or d > max_dist:
                return -1
            raw_interest = -4 * ((break_even / d) ** 12 - (break_even / d) ** 6)
            max_interest = 2 ** (1 / 6) * break_even
            capped_interest = raw_interest / max_interest
            interest += capped_interest

        return interest / len(building_locations)


def gen_closest_distance_comparator(point):
    return lambda building: math.dist(point, (building.x, building.z))
