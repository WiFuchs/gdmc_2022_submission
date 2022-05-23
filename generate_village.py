import numpy as np
from gdpc import interface
from village_planner import VillagePlanner, BuildArea
from build_road import build_road
from prep_land import prep_land
from helper_functions import *

def driver():
    """
    Function that drives the village generation.
    """
    AROUND_PLAYER = True
    w = 256
    h = 256
    if AROUND_PLAYER:
        interface.runCommand("say start")
        resp = interface.runCommand(f"execute at @p run setbuildarea ~0 0 ~0 ~{w} 256 ~{h}")
        interface.runCommand("say end")

    sx, sy, sz, ex, ey, ez = interface.requestBuildArea()
    print(f'Coords: {sx},{sy},{sz} - {ex},{ey},{ez}')
    # HARD CODE - 259,0,205 - 515,256,461

    VISUALIZE_BUILD_AREA = True
    if VISUALIZE_BUILD_AREA:
        build_perimeter_around_BA((sx, sy, sz), (ex, ey, ez))


    # interface.runCommand(f"tp @a {sx} {256} {sz}")
    
    # Create build area object
    build_area = BuildArea(sx, sz, ex, ez)

    # Create planner object and find the building seeds
    planner = VillagePlanner(build_area)

    # Saves the building / road locations for debugging (So they don't randomly generate everytime)
    USE_HARD_CODED_BUILDINGS_AND_ROADS = False
    if USE_HARD_CODED_BUILDINGS_AND_ROADS:
        building_locations, road_map = hard_code_buildings_and_roads(planner, False)
    else:    
        planner.seed_buildings(goal_buildings=24)
        building_locations = planner.building_locations
        road_map = planner.road_map
    

    # For all buildings, prep the land and build a base
    prep_land(building_locations, planner)
    


if __name__ == '__main__':
    driver()
