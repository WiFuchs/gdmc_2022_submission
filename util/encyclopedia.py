from abc import ABC, abstractmethod
import math

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from village_planner import BuildArea


class BuildingEncyclopedia:
    pass


class BuildingEquation(ABC):
    @abstractmethod
    def calculate_interest(self, build_area: 'BuildArea', x, z) -> float:
        pass


class AttractRepulse(BuildingEquation):
    """Lennard-Jones Potential function that repels at close distances and attracts at larger distances.
        Break_even is the distance where the function switches from repelling to attracting
    """

    def __init__(self, min_dist: int, max_dist: int, break_even: int):
        self.min_dist = min_dist
        self.max_dist = max_dist
        self.break_even = break_even
        self.closest_interest = None

    def calculate_interest(self, build_area: 'BuildArea', x, z):
        """Use an attraction-repulsion function to calculate the interest of building at this point"""
        if self.closest_interest is None:
            return 0            # if no closest interest set, return no interest

        d = math.dist(self.closest_interest, (x,z))
        # if the distance is out of bounds, this is not a suitable building location
        if d < self.min_dist or d > self.max_dist:
            return -1
        raw_interest = -4 * ((self.break_even / d) ** 12 - (self.break_even / d) ** 6)
        return raw_interest

    def set_point_of_interest(self, x, z, set_to_none = False):
        self.closest_interest = None if set_to_none else (x, z)