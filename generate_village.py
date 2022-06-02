# Python imports
import numpy as np
from gdpc import interface
import lib.interfaceUtils as iu
import util.worldModification as worlModif

# Local imports
from village_planner import VillagePlanner, BuildArea
from util.encyclopedia import BuildingType
from prep_land import prep_land
from build_road import build_roads
from generate_structure import generate_structures
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

    # Create build area object
    build_area = BuildArea(sx, sz, ex, ez)

    # Create list of building types
    # NOTE: names here must match names in data/structure_relationshipos/structure_attraction.csv
    hayBale = BuildingType("haybale", 8)
    farm = BuildingType("farm", 13)
    small_house = BuildingType("small_house", 10)
    medium_house = BuildingType("medium_house", 15)
    townhall = BuildingType("townhall", 20)
    windmill = BuildingType("windmill", 28)
    cemetary = BuildingType("graveyard", 24)
    tavern = BuildingType("tavern", 11)
    adventure = BuildingType("enforcement", 15)
    misc = BuildingType("misc", 10)

    building_types = [hayBale, farm, small_house, medium_house, townhall, windmill, cemetary, tavern, adventure, misc]

    # Create planner object and find the building seeds
    planner = VillagePlanner(build_area, building_types, "data/structure_relationships/structure_attraction.csv")

    # Saves the building / road locations for debugging (So they don't randomly generate everytime)
    USE_HARD_CODED_BUILDINGS_AND_ROADS = False
    if USE_HARD_CODED_BUILDINGS_AND_ROADS:
        building_locations, road_map = hard_code_buildings_and_roads(planner, False)
    else:
        planner.seed_buildings(goal_buildings=10)
        building_locations = planner.building_locations
        road_map = planner.road_map

    # For all buildings, prep the land and build a base
    prep_land(building_locations, planner)

    # Build structures at all building seeds
    referenceCoordinates = [sx, sy, sz]
    generate_structures(
        building_locations,
        referenceCoordinates
    )

    # Build roads
    lamp_locations = build_roads(build_area.worldslice, road_map)

    # @Miko: The above lamp_locations should have all the global coordinates of where to put lamps. They should be in (x,y,z) form.


if __name__ == '__main__':
    driver()
