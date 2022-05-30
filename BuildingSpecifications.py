from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from util.encyclopedia import BuildingType


class Building:
    """This class represents a building at a specific point.
    """
    def __init__(self, point: Tuple[int, int], building_type: 'BuildingType'):
        self.x = point[0]
        self.y = None
        self.z = point[1]
        self.rotation = 0
        self.building_type = building_type
