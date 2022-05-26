from abc import ABC, abstractmethod
import math
import numpy as np
from typing import TYPE_CHECKING, List, Tuple
from BuildingSpecifications import Building

if TYPE_CHECKING:
    from village_planner import BuildArea


class BuildingEquation(ABC):
    @abstractmethod
    def calculate_interest(self, build_area: 'BuildArea', building_locations: List[Building], x, z) -> float:
        pass


class BuildingType:
    def __init__(self, name, equations: List[BuildingEquation], weights, radius):
        self.name = name
        self.equations: List[BuildingEquation] = equations
        self.weights = np.array(weights)
        self.radius = radius
        self.structure = None
        self.orientation = None

    def calc_interest(self, build_area: 'BuildArea', point, building_locations: List[Building]) -> (
            float, Tuple[int, int]):
        """Calculate the interest of building at this point based on location and the world state
            :returns
                float in the range 0-1
        """
        assert self.weights.sum() == 1.0  # Weights must be normalized
        interest_vals = np.array([eq.calculate_interest(build_area, building_locations, point[0], point[1]) for eq in self.equations])
        if -1 in interest_vals:
            return 0, None
        interest = np.multiply(interest_vals, self.weights).sum()
        assert interest <= 1.0
        if building_locations:
            return interest, (building_locations[-1].x, building_locations[-1].z)
        return interest, None


def gen_closest_distance_comparator(point):
    return lambda building: math.dist(point, (building.x, building.z))


class AttractRepulse(BuildingEquation):
    """Lennard-Jones Potential function that repels at close distances and attracts at larger distances.
        Break_even is the distance where the function switches from repelling to attracting
    """

    def __init__(self, min_dist: int, max_dist: int, break_even: int):
        self.min_dist = min_dist
        self.max_dist = max_dist
        self.break_even = break_even

    def calculate_interest(self, build_area: 'BuildArea', building_locations: List[Building], x, z):
        """Use an attraction-repulsion function to calculate the interest of building at this point"""
        if not building_locations:
            return 0.5

        interest = 0
        # loop over all buildings and calculate interest from them
        for building in building_locations:
            d = math.dist((building.x, building.z), (x, z))
            # if the distance to any house is out of bounds, this is not a suitable building location
            if d < self.min_dist or d > self.max_dist:
                return -1
            raw_interest = -4 * ((self.break_even / d) ** 12 - (self.break_even / d) ** 6)
            max_interest = 2**(1/6)*self.break_even
            capped_interest = raw_interest / max_interest
            interest += capped_interest

        return interest / len(building_locations)
