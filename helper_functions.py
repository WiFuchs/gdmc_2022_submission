"""
This script will contain helper functions for our village generator that we don't want to include in the generate_village.py script.
"""

from json import load
from gdpc import geometry as GEO
from gdpc import interface as INTF
from gdpc import toolbox as TB
from gdpc import worldLoader as WL

def convert_coords(coord, start):
    """
    Converts local coordinates to coordinates that coordinate to blocks in the minecraft world.
    Examples: If build area is (300, 0, 450) - (600, 256, 750)"
        - convert_coords((0, 0)) -> (300, 450)
        - convert_coords((100, 100)) -> (400, 550)
    Input:
        coord (tuple): The coordinate we are going to convert from local to global.
        start (tuple): The starting coordinates of our build area
    Ouput:
        (tuple): The local-to-global converted coordinate.
    """
    local_x, local_z = coord

    return (local_x + start[0], local_z + start[1])

def load_buildings_and_roads(filename):
    """
    Loads in hard-coded building locations and roads.
    """
    with open(filename, 'r') as fp:
        lines = fp.read()
    roads, building_locations = lines.split(u'|')
    
    # Parse out building locations
    building_locations = building_locations.strip(r'{}').split('), ') 
    building_locations = [(i.replace('(', '').replace(')', '')) for i in building_locations]
    building_locations = [(int(i.split(', ')[0]), int(i.split(', ')[1])) for i in building_locations]

    #Parse Roads
    roads = [row for row in roads.split('\n')]
    roads = [row.strip('][').split(', ') for row in roads][:-1]
    roads = [[int(this_val) for this_val in row] for row in roads]
    
    return building_locations, roads

def build_perimeter_around_BA(start, end):
    """
    Builds high corners around the build area for visualization purposes.
    Inputs:
        start (tuple): (x,y,z) Coordinates of our starting point.
        end (tuple): (x,y,z) Coordinates of our ending point.
    """
    GEO.placeCuboid(start[0], 0, start[2], start[0], 256, start[2], 'oak_planks') 
    GEO.placeCuboid(start[0], 0, end[2], start[0], 256, end[2], 'oak_planks') 
    GEO.placeCuboid(end[0], 0, start[2], end[0], 256, start[2], 'oak_planks') 
    GEO.placeCuboid(end[0], 0, end[2], end[0], 256, end[2], 'oak_planks') 
    

def hard_code_buildings_and_roads(planner, save_buildings_and_roads):
    if save_buildings_and_roads:
        roads = []
        with open('hard_codings.txt', 'w') as fp:
                for row in planner.road_map:
                    new_row = [(1 if i == True else 0) for i in row]
                    roads.append(new_row)
                    fp.write(str(new_row))
                    fp.write('\n')
                fp.write('|')
                fp.write(str(planner.building_locations))
        return planner.building_locations, roads
    else:
        # Load Buildings and roads from file
        return load_buildings_and_roads('hard_codings.txt')
