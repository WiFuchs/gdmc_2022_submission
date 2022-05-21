import math
import random
from gdpc import worldLoader
from gdpc import geometry
from queue import PriorityQueue

from util.encyclopedia import BuildingEncyclopedia, AttractRepulse
from util.map import Map
import cv2
import numpy as np


class BuildArea:
    def __init__(self, sx, sz, ex, ez):
        self.worldslice = worldLoader.WorldSlice(sx, sz, ex + 1, ez + 1)  # this takes a while
        self.heightmap_no_trees = Map.calc_clear_heightmap(self.worldslice)
        self.start = (sx, sz)
        self.end = (ex, ez)
        self.length_x = ex - sx
        self.length_z = ez - sz
        self.water_mask = np.array(np.where(self.worldslice.heightmaps['OCEAN_FLOOR'] < self.heightmap_no_trees, 0, 1),
                                   dtype="uint8")

        assert self.length_x > 0
        assert self.length_z > 0

    def local_to_global(self, x: int, z: int) -> (int, int):
        return x + self.start[0], z + self.start[1]

    def get_random_point(self):
        return random.randrange(self.length_x), random.randrange(self.length_z)


class VillagePlanner:
    def __init__(self, build_area: BuildArea):
        self.build_area = build_area

        # get slope using max and min elevation within kernel
        kernel = np.ones((5, 5), 'uint8')
        local_max_heights = cv2.dilate(self.build_area.heightmap_no_trees, kernel, iterations=1)
        local_min_heights = cv2.erode(self.build_area.heightmap_no_trees, kernel, iterations=1)
        slope = local_max_heights - local_min_heights

        # approximate slope with median blur difference
        # median = cv2.medianBlur(self.build_area.heightmap_no_trees, 11)
        # difference = np.array(self.build_area.heightmap_no_trees - median, dtype="uint8")
        # self.buildable_points = np.where((difference == 0) & (self.build_area.water_mask == 1),
        #                                  self.build_area.heightmap_no_trees, 0)

        self.buildable_points = np.where((slope <= 2) & (self.build_area.water_mask == 1),
                                         self.build_area.heightmap_no_trees, 0)
        self.build_map = np.copy(self.buildable_points)  # build map is purely for displaying buildings/roads/etc
        self.road_map = np.zeros_like(self.buildable_points, dtype="bool")
        self.building_locations = set()

    def display_map(self):
        median = cv2.medianBlur(self.build_area.heightmap_no_trees, 11)
        difference = np.array(self.build_area.heightmap_no_trees - median, dtype="uint8")

        kernel = np.ones((5, 5), 'uint8')
        local_max_heights = cv2.dilate(self.build_area.heightmap_no_trees, kernel, iterations=1)
        local_min_heights = cv2.erode(self.build_area.heightmap_no_trees, kernel, iterations=1)
        slope = local_max_heights - local_min_heights

        cv2.imshow('slope', slope)
        cv2.imshow('original', self.build_area.heightmap_no_trees)
        cv2.imshow('blurred', median)
        cv2.imshow('difference', difference + 127)
        cv2.imshow('water', self.build_area.water_mask * 255)
        cv2.imshow('build points', self.build_map)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def check_buildable(self, point, size) -> bool:
        row_mask = np.array(
            [1 if (i - point[0]) ** 2 < size ** 2 else 0 for i in range(self.buildable_points.shape[0])], dtype=bool)
        col_mask = np.array(
            [1 if (i - point[1]) ** 2 < size ** 2 else 0 for i in range(self.buildable_points.shape[1])], dtype=bool)
        surrounding_area = self.buildable_points[np.ix_(row_mask, col_mask)]
        if np.any(surrounding_area == 0):
            return False
        return True

    def add_building_to_road(self, building_x: int, building_z: int, closest_building):
        """Add a building to the road network. Uses A*"""
        nodes = [[None for _ in range(self.build_area.length_x)] for _ in range(self.build_area.length_z)]
        open = PriorityQueue()

        start_node = PathNode(building_x, building_z)
        start_node.g_score = 0
        nodes[building_x][building_z] = start_node
        open.put(start_node)

        while not open.empty():
            cur_node = open.get()

            if closest_building == cur_node.pos:
                road = cur_node.reconstruct_path()
                for road_pixel in road:
                    self.road_map[road_pixel] = 1
                return

            # check neighbors in all possible directions
            for x_off, z_off, cost in [(-1, -1, 1.4), (-1, 1, 1.4), (1, -1, 1.4), (1, 1, 1.4), (1, 0, 1), (-1, 0, 1),
                                       (0, 1, 1), (0, -1, 1)]:
                # make sure that we are staying within the build area
                if 0 < cur_node.x + x_off < self.build_area.length_x - 1 and 0 < cur_node.z + z_off < self.build_area.length_z - 1:
                    if nodes[cur_node.x + x_off][cur_node.z + z_off] is None:
                        nodes[cur_node.x + x_off][cur_node.z + z_off] = PathNode(cur_node.x + x_off, cur_node.z + z_off)
                    neighbor = nodes[cur_node.x + x_off][cur_node.z + z_off]
                    tentative_g = cur_node.g_score + cur_node.get_slope_cost(self.build_area, self.road_map, neighbor)

                    if tentative_g < neighbor.g_score:
                        # This is the new best path to here
                        neighbor.came_from = cur_node
                        neighbor.g_score = tentative_g
                        neighbor.f_score = tentative_g + neighbor.calc_h_score(self.build_area, closest_building)
                        open.put(neighbor)

    def seed_buildings(self, goal_buildings: int, display_map=True):
        """
        Wipe the old building seeds and create new building seeds.
        This populates self.building_locations
        """
        num_buildings = 0
        self.building_locations = set()
        attraction_eq = AttractRepulse(min_dist=7, max_dist=100, break_even=17)
        retries = 0
        force_buildings = True  # force the number of buildings to be exactly goal_buildings
        while num_buildings < goal_buildings and (retries < goal_buildings * 200 or force_buildings):
            retries += 1
            point = self.build_area.get_random_point()
            height = self.buildable_points[point]
            # if this is not a buildable point, pick a new one
            if height == 0 or not self.check_buildable(point, 7):
                continue

            closest_point = None
            if self.building_locations:
                closest_point = sorted(self.building_locations, key=lambda bp: math.dist(bp, point))[0]
                attraction_eq.set_point_of_interest(closest_point[0], closest_point[1])

            interest = attraction_eq.calculate_interest(self.build_area, point[0], point[1])
            if interest == -1:
                continue
            build_probability = random.uniform(interest, 1.0)
            if build_probability >= 0.9:
                # add the new building
                self.building_locations.add(point)
                num_buildings += 1
                retries = 0

                # add a road to the new building if it is not the first
                if closest_point is not None:
                    self.add_building_to_road(point[0], point[1], closest_point)

        if display_map:

            # mark building locations in white
            for pt in self.building_locations:
                self.build_map[pt] = 255
                self.build_map = cv2.circle(self.build_map, (pt[1], pt[0]), 7, (255, 255, 255))

            # mark roads on build map
            self.build_map = np.where(self.road_map == 1, 255, self.build_map)

            cv2.imshow("build map", self.build_map)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


class PathNode:
    def __init__(self, x: int, z: int):
        self.x = x
        self.z = z
        self.f_score = np.inf
        self.g_score = np.inf
        self.came_from = None

    def __lt__(self, other: 'PathNode'):
        return self.f_score < other.f_score

    def calc_h_score(self, build_area: BuildArea, goal):
        D = 1  # Cost of moving to an adjacent grid square
        D2 = 1.4  # Cost of moving diagonally
        dx = abs(self.x - goal[0])
        dy = abs(self.z - goal[1])
        distance = D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)

        # TODO how do I account for slope, water crossings, etc?
        return distance

    @property
    def pos(self):
        return self.x, self.z

    def reconstruct_path(self):
        assert self.pos is not None
        if self.came_from is not None:
            path = self.came_from.reconstruct_path()
            path.append(self.pos)
            return path
        return [self.pos]

    def get_slope_cost(self, build_area: BuildArea, road_map, other):
        """Get cost of moving to an adjacent block. Steepness is penalized, road re-use is rewarded"""
        steepness = abs(int(build_area.heightmap_no_trees[self.pos]) - int(build_area.heightmap_no_trees[other.pos]))
        steepness = steepness ** steepness
        road_exists = road_map[self.pos]
        if road_exists:
            steepness = 0
        return steepness
