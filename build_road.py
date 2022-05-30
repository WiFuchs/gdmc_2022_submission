"""
Author: Keon Roohparvar
Date: 5-9-22

This script serves to prepare land for buildings. It does this by receiving coordinates of land it is going to 'prepare' and a certain Y height,
and the script will ensure that the cooridinates have a solid, flat ground under them at the specified Y height. 
"""

# Imports
from distutils.command.build import build
from random import randint

from gdpc import geometry as GEO
from gdpc import interface as INTF
from gdpc import toolbox as TB
from gdpc import worldLoader as WL

from helper_functions import convert_coords

def build_roads(WORLDSLICE, road_map):
    roads = []

    # find roads by parsing the road_map
    x = 0
    z = 0
    for z in range(road_map.shape[0]):
        for x in range(road_map.shape[1]):
            if road_map[(x,z)] != False:
                roads.append((x,z))
    
    # Bookkeeping for lamp index
    lamps = []
    BUILD_LAMP_EVERY = 40
    this_lamp_ind = BUILD_LAMP_EVERY

    # Build blocks at all road points
    for road in roads:
        this_lamp_ind = this_lamp_ind - 1
        this_lamp_ind = (this_lamp_ind if this_lamp_ind >= 0 else BUILD_LAMP_EVERY)
        this_lamp_location = build_road(WORLDSLICE, road[0], road[1], 'oak_planks', (this_lamp_ind == 0), find_road_orientation(road, road_map)) 
        if this_lamp_location != None:
            lamps.append(this_lamp_location)

    return lamps

def find_road_orientation(road, road_map):
    this_x, this_z = road
    
    # Check x direction
    if (road_map[(this_x-1, this_z)] != False if this_x > 0 else False) or (road_map[(this_x+1, this_z)] != False if this_x < len(road_map) else False):
        return 'along_x'

    # Check z direction
    if (road_map[(this_x, this_z-1)] != False if this_z > 0 else False) or (road_map[(this_x, this_z+1)] != False if this_z < len(road_map[0]) else False):
        return 'along_z'


def point_valid(point, heightmap):
    x,z = point
    if x > heightmap.shape[0]:
        return False
    if z > heightmap.shape[1]:
        return False
    if x < 0 or z < 0:
        return False
    return True
        

def build_road(WORLDSLICE, x, z, base_block, build_lamp, direction=None):
    """
    This function will create a road from point (x1, _, z1) to (x2, _, z2). It places a block based off of
    the string passed into 'base_block', and it creates 3-length roads with the middle being the straight 
    line between the two points passed in.

    Input:
        WORLDSLICE (object): The worldslice object of our build area
        x1 (int): X cordinate of our starting point for our road.
        z1 (int): Z cordinate of our starting point for our road.
        x2 (int): X cordinate of our starting point for our road.
        z2 (int): Z cordinate of our starting point for our road.
        base_block (string): The type of block we want as the base rectangle
    """

    heights = WORLDSLICE.heightmaps['MOTION_BLOCKING_NO_LEAVES']
    start_x, start_z, _, _ = WORLDSLICE.rect

    this_y = heights[(x, z)] 
    global_x, global_z = convert_coords((x,z), (start_x, start_z))
    INTF.placeBlock(global_x, this_y-1, global_z, base_block)

    if direction == 'along_z':
        if x < len(heights):
            INTF.placeBlock(global_x+1, this_y-1, global_z, base_block)
        if x > 0:   
            INTF.placeBlock(global_x-1, this_y-1, global_z, base_block)
            if build_lamp:
                return (global_x-1, this_y-1, global_z)
        return None
    
    if direction == 'along_x':
        if z < len(heights[0]):
            INTF.placeBlock(global_x, this_y-1, global_z+1, base_block)
        if z > 0:   
            INTF.placeBlock(global_x-1, this_y-1, global_z-1, base_block)
            if build_lamp:
                return (global_x-1, this_y-1, global_z)
        return None

    # If it is not along the x or z direction, it is diagonal. We then do a 3x3 box around it.
    block_points = [(x-1, z-1), (x, z-1), (x+1, z-1), (x-1, z), (x+1, z), (x-1, z+1), (x, z+1), (x+1, z+1)]
    for new_point in block_points:
        # Ensures our point is in the boudaries
        if point_valid(new_point, heights):
            this_global_x, this_global_z = convert_coords(new_point, (start_x, start_z))
            INTF.placeBlock(this_global_x, this_y-1, this_global_z, base_block)
    if build_lamp and point_valid(block_points[0], heights):
        lamp_x, lamp_z = convert_coords(block_points[0], (start_x, start_z))
        return (lamp_x, this_y-1, lamp_z)
    return None




    """
    # Road in x direction
    if z1 == z2:
        for x in range(x1, x2+1):
            # Need to use local_x and local_z to index into height map
            local_x = x - start_x 
            local_z = z1 - start_z

            # Get the height of this point
            this_y = heights[(local_x, local_z)]

            # Place three blocks with the specified input block as the middle
            INTF.placeBlock(x, this_y-1, z1-1, base_block)
            INTF.placeBlock(x, this_y-1, z1, base_block)
            INTF.placeBlock(x, this_y-1, z1+1, base_block)
    
    # Road in z direction
    elif x1 == x2:
        for z in range(z1, z2+1):
            # Need to use local_x and local_z to index into height map
            local_x = x1 - start_x 
            local_z = z - start_z

            # Get the height of this point
            this_y = heights[(local_x, local_z)]

            # Place three blocks with the specified input block as the middle
            INTF.placeBlock(x1-1, this_y-1, z, base_block)
            INTF.placeBlock(x1, this_y-1, z, base_block)
            INTF.placeBlock(x1+1, this_y-1, z, base_block)

    # Diagonal road?
    else:
        print('Diagonal road not supported (yet?)')
    """
 



# BELOW IS USED FOR TESTING
if __name__ == '__main__':
    # STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.requestBuildArea()  # BUILDAREA
    STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.setBuildArea(136, 50, 361, 179, 94, 417)
    print(f"Start x: {STARTX}")

    WORLDSLICE = WL.WorldSlice(STARTX, STARTZ, ENDX + 1, ENDZ + 1)
    build_road(WORLDSLICE, 146, 369, 156, 369, 'oak_planks')
    build_road(WORLDSLICE, 156, 369, 156, 389, 'oak_planks')
    

