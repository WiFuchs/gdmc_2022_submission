"""
Author: Keon Roohparvar
Date: 5-9-22

This script serves to prepare land for buildings. It does this by receiving coordinates of land it is going to 'prepare' and a certain Y height,
and the script will ensure that the cooridinates have a solid, flat ground under them at the specified Y height. 
"""

# Imports
from lib2to3.pytree import convert
from random import randint

import numpy as np

from gdpc import geometry as GEO
from gdpc import interface as INTF
from gdpc import toolbox as TB
from gdpc import worldLoader as WL

from helper_functions import convert_coords

def prep_land(buildings, planner):
    """
    This function will go throguh all buildings 
    """
    for building in buildings:
        this_x, this_z = building
        print(f'This building is at {this_x} x {this_z}')
        prep_single_building(planner.build_area.worldslice, this_x, this_z, this_x+5, this_z+5, 'oak_planks', 10)


def prep_single_building(WORLDSLICE, x1, z1, x2, z2, base_block, height):
    """
    This function simply receives a rectangle and a desired y level, and places a rectangle of blocks there, 
    while clearing a number of blocks above specified by the height input. 

    Input:
        WORLDSLICE (object): The worldslice object of our build area
        x1 (int): Starting x point of our base rectangle.
        z1 (int): Starting z point of our base rectangle.
        x2 (int): Ending x point of our base rectangle.
        x2 (int): Ending z point of our base rectangle.
        base_block (string): The type of block we want as the base rectangle
        height (int): This value specifies how large the y value of our building is going to be.
    """
    heights = WORLDSLICE.heightmaps['MOTION_BLOCKING_NO_LEAVES']
    start_x, start_z, _, _ = WORLDSLICE.rect

    print(f"Heights: {heights}")

    # Find desired y height
    heights_list = []
    for z in range(z1, z2+1):
        for x in range(x1, x2+1):
            heights_list.append(heights[(x, z)])
    desired_y = round(np.mean(np.array(heights_list))) - 1

    for z in range(z1, z2+1):
        for x in range(x1, x2+1):
            # Need to use local_x and local_z to index into height map
            global_x, global_z = convert_coords((x,z), (start_x, start_z))


            # Prints all heights for this chunk of land
            # print(f"({x}, {z}): {heights[(local_x, local_z)]}")

            INTF.placeBlock(global_x, desired_y, global_z, base_block)
    
    # Clear blocks above the desired y in our land chunk
    global_start = convert_coords((x1, z1), (start_x, start_z))
    global_end = convert_coords((x2, z2), (start_x, start_z))
    GEO.placeCuboid(global_start[0], desired_y+1, global_start[1], global_end[0], desired_y+height, global_end[1], 'air') 



# BELOW IS USED FOR TESTING
if __name__ == '__main__':
    STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.requestBuildArea()  # BUILDAREA
    # STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.setBuildArea(136, 63, 361, 179, 94, 417)
    print(f"Start x: {STARTX}")

    WORLDSLICE = WL.WorldSlice(STARTX, STARTZ, ENDX + 1, ENDZ + 1)
    prep_land(WORLDSLICE, 161, 394, 167, 401, 63, 'oak_planks', 20)


