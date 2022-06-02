import math
import random
from gdpc import worldLoader
from gdpc import geometry
from queue import PriorityQueue
import typing
from BuildingSpecifications import Building
from util.encyclopedia import BuildingType, BuildingEncyclopedia
from util.map import Map
import cv2
import numpy as np
import csv


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
    def __init__(self, build_area: BuildArea, building_types: typing.List[BuildingType], attraction_file):
        self.build_area = build_area

        self.building_encyclopedia = BuildingEncyclopedia(attraction_file)

        # get slope using max and min elevation within kernel
        kernel = np.ones((5, 5), 'uint8')
        local_max_heights = cv2.dilate(self.build_area.heightmap_no_trees, kernel, iterations=1)
        local_min_heights = cv2.erode(self.build_area.heightmap_no_trees, kernel, iterations=1)
        slope = local_max_heights - local_min_heights

        self.buildable_points = np.where((slope <= 2) & (self.build_area.water_mask == 1),
                                         self.build_area.heightmap_no_trees, 0)
        self.build_map = np.zeros_like(self.buildable_points, dtype="bool")
        self.road_map = np.zeros_like(self.buildable_points, dtype="bool")
        self.building_locations: typing.List[Building] = []
        self.building_types = building_types
        self.bridges = []       # list of (x,y,z) points on bridges

    def check_buildable(self, point, size) -> bool:
        row_mask = np.array(
            [1 if (i - point[0]) ** 2 < size ** 2 else 0 for i in range(self.buildable_points.shape[0])], dtype=bool)
        col_mask = np.array(
            [1 if (i - point[1]) ** 2 < size ** 2 else 0 for i in range(self.buildable_points.shape[1])], dtype=bool)
        surrounding_area = self.buildable_points[np.ix_(row_mask, col_mask)]
        if np.any(surrounding_area == 0):
            return False
        return True

    def add_building_to_road(self, building_x: int, building_z: int):
        """Add a building to the road network. Uses BFS where weights are the distances"""
        nodes = [[None for _ in range(self.build_area.length_x)] for _ in range(self.build_area.length_z)]
        open = PriorityQueue()
        bridge_radius = 20
        start_node = PathNode(building_x, building_z)
        start_node.g_score = 0
        nodes[building_x][building_z] = start_node
        open.put(start_node)

        while not open.empty():
            cur_node = open.get()

            if cur_node.pos != start_node.pos and (
                    self.road_map[cur_node.pos] == 1 or self.build_map[cur_node.pos] == 1):
                roads = cur_node.reconstruct_path()
                bridges = cur_node.reconstruct_bridges()
                for road_pixel in roads:
                    self.road_map[road_pixel] = 1
                for bridge_start, bridge_end in bridges:
                    direction = "z" if bridge_start[0] == bridge_end[0] else "x"
                    height = self.build_area.heightmap_no_trees[bridge_start]
                    if direction == "z":
                        start_z = min(bridge_start[1], bridge_end[1])
                        end_z = max(bridge_start[1], bridge_end[1])
                        bridge_points = [(bridge_start[0], height, z) for z in range(start_z, end_z + 1)]
                    else:
                        start_x = min(bridge_start[0], bridge_end[0])
                        end_x = max(bridge_start[0], bridge_end[0])
                        bridge_points = [(x, height, bridge_start[1]) for x in range(start_x, end_x + 1)]

                    self.bridges.append((bridge_points, direction))
                return

            need_bridges = False

            # check neighbors in all possible directions for surface roads
            for x_off, z_off, cost in [(-1, -1, 1.4), (-1, 1, 1.4), (1, -1, 1.4), (1, 1, 1.4), (1, 0, 1), (-1, 0, 1),
                                       (0, 1, 1), (0, -1, 1)]:
                # make sure that we are staying within the build area
                if 0 < cur_node.x + x_off < self.build_area.length_x - 1 and 0 < cur_node.z + z_off < self.build_area.length_z - 1:
                    if nodes[cur_node.x + x_off][cur_node.z + z_off] is None:
                        nodes[cur_node.x + x_off][cur_node.z + z_off] = PathNode(cur_node.x + x_off, cur_node.z + z_off)
                    neighbor = nodes[cur_node.x + x_off][cur_node.z + z_off]
                    slope_cost = cur_node.get_slope_cost(self.build_area, self.road_map,
                                                         neighbor)
                    tentative_g = cur_node.g_score + cost * slope_cost

                    if slope_cost == np.inf:
                        need_bridges = True

                    # TODO do we really need the f score anymore? We aren't calculating a h score so f == g
                    if tentative_g < neighbor.g_score:
                        # This is the new best path to here
                        neighbor.came_from = cur_node
                        neighbor.g_score = tentative_g
                        neighbor.f_score = tentative_g  # + neighbor.calc_h_score(self.build_area)
                        neighbor.type = "flat"
                        open.put(neighbor)

            # check bridges of length 3 to bridge_radius
            if need_bridges:
                start_height = self.build_area.heightmap_no_trees[cur_node.pos]
                for r in range(3, bridge_radius, 3):
                    for dir in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        x_off = dir[0] * r
                        z_off = dir[1] * r
                        if 0 < cur_node.x + x_off < self.build_area.length_x - 1 and 0 < cur_node.z + z_off < self.build_area.length_z - 1:
                            # can only build a bridge if the start and end heights are the same (or similar???)
                            end_x = cur_node.x + x_off
                            end_z = cur_node.z + z_off
                            delta_h = start_height - self.build_area.heightmap_no_trees[end_x, end_z]
                            on_land = self.build_area.water_mask[end_x, end_z] == 1
                            if delta_h != 0 or not on_land:
                                continue

                            if nodes[cur_node.x + x_off][cur_node.z + z_off] is None:
                                nodes[cur_node.x + x_off][cur_node.z + z_off] = PathNode(cur_node.x + x_off,
                                                                                         cur_node.z + z_off)
                            end_node = nodes[cur_node.x + x_off][cur_node.z + z_off]
                            tentative_g = cur_node.g_score + cur_node.get_bridge_cost(self.build_area, dir, end_node)
                            if tentative_g < end_node.g_score:
                                # This is the new best path to here
                                end_node.came_from = cur_node
                                end_node.g_score = tentative_g
                                end_node.f_score = tentative_g
                                end_node.type = "bridge"
                                open.put(end_node)

    def seed_buildings(self, goal_buildings: int, display_map=True):
        """
        Wipe the old building seeds and create new building seeds.
        This populates self.building_locations
        """
        num_buildings = 0
        self.building_locations: typing.List[Building] = []
        retries = 0
        force_buildings = False  # force the number of buildings to be goal_buildings, ok for testing, may inf loop
        while num_buildings < goal_buildings and (retries < goal_buildings * 400 or force_buildings):
            retries += 1
            point = self.build_area.get_random_point()
            height = self.buildable_points[point]
            # if this is not a buildable point, pick a new one
            if height == 0:
                continue

            # Calculate the interest for each building type. Build the first one that passes the test (TODO should
            #  this test them in order of interest?)
            for building_type in self.building_types:
                if not self.check_buildable(point, building_type.radius):
                    continue

                interest = building_type.calc_interest(self.build_area, point, self.building_locations,
                                                       self.building_encyclopedia)
                if interest == 0:
                    continue  # unsuitable building location

                build_probability = random.uniform(interest, 1.0)
                if build_probability >= 0.9:
                    # add the new building
                    self.building_locations.append(Building(point, building_type))
                    self.build_map[point] = 1  # TODO extend this to maybe fill in the whole building plot?
                    num_buildings += 1
                    retries = 0

                    # add a road to the new building, if there are other buildings
                    if len(self.building_locations) > 1:
                        self.add_building_to_road(point[0], point[1])

        if display_map:
            new_map = np.copy(self.buildable_points)
            # mark building locations in white
            for building in self.building_locations:
                new_map[(building.x, building.z)] = 255
                new_map = cv2.circle(new_map, (building.z, building.x), building.building_type.radius, (255, 255, 255))

            # mark roads on build map
            new_map = np.where(self.road_map == 1, 255, new_map)

            bridges_map = np.copy(self.buildable_points)
            for bridge_points, direction in self.bridges:
                for x, y, z in bridge_points:
                    bridges_map[(x, z)] = 255

            cv2.imshow("bridges_map", bridges_map.astype(np.uint8))
            cv2.imshow("everything map", new_map.astype(np.uint8))
            cv2.waitKey(0)
            cv2.destroyAllWindows()


bridge_count = 0


class PathNode:
    def __init__(self, x: int, z: int):
        self.x = x
        self.z = z
        self.f_score = np.inf
        self.g_score = np.inf
        self.came_from = None
        self.type = None

    def __lt__(self, other: 'PathNode'):
        return self.f_score < other.f_score

    # def calc_h_score(self, build_area: BuildArea, goal):
    #     D = 1  # Cost of moving to an adjacent grid square
    #     D2 = 1.4  # Cost of moving diagonally
    #     dx = abs(self.x - goal[0])
    #     dy = abs(self.z - goal[1])
    #     distance = D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
    #
    #     # TODO how do I account for slope, water crossings, etc?
    #     return distance

    @property
    def pos(self):
        return self.x, self.z

    def reconstruct_bridges(self):
        assert self.pos is not None
        if self.came_from is not None:
            bridges = self.came_from.reconstruct_bridges()
            if self.type == "bridge":
                bridges.append((self.pos, self.came_from.pos))
            return bridges
        return []

    def reconstruct_path(self):
        assert self.pos is not None
        if self.came_from is not None:
            path = self.came_from.reconstruct_path()
            path.append(self.pos)
            if self.type == "bridge":
                global bridge_count
                bridge_count += 1
                print(f"adding bridge {bridge_count} - {self.pos}")
            return path
        return [self.pos]

    def get_slope_cost(self, build_area: BuildArea, road_map, other):
        """Get cost of moving to an adjacent block. Steepness is penalized, road re-use is rewarded"""
        steepness = abs(int(build_area.heightmap_no_trees[self.pos]) - int(build_area.heightmap_no_trees[other.pos]))
        cost = steepness + 1
        # if the grade is not traversable, we can't build a surface road. Need bridge or tunnel
        if steepness >= 2 or not build_area.water_mask[other.pos]:
            cost = np.inf

        road_exists = road_map[self.pos]
        if road_exists:
            cost = 0
        return cost

    def get_bridge_cost(self, build_area: BuildArea, dir, other):
        """Get cost of building a bridge directly to this node """
        cost = 0
        cur_x = self.x + dir[0]
        cur_z = self.z + dir[1]
        height = build_area.heightmap_no_trees[self.pos]

        # march along bridge path to determine cost of building a bridge/tunnel
        while cur_x != other.x or cur_z != other.z:
            delta_h = abs(height - build_area.worldslice.heightmaps['OCEAN_FLOOR'][(cur_x, cur_z)])
            # cost is the height plus the cost of building a road on flat ground
            cost += delta_h
            cost += 2  # building a bridge should be more expensive than building a regular road

            cur_x += dir[0]
            cur_z += dir[1]

        return cost
