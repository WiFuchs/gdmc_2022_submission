"""
Author: Keon Roohparvar
Date: 5-9-22

This script serves to prepare land for buildings. It does this by receiving coordinates of land it is going to 'prepare' and a certain Y height,
and the script will ensure that the cooridinates have a solid, flat ground under them at the specified Y height. 
"""

# Imports
from random import randint

from gdpc import geometry as GEO
from gdpc import interface as INTF
from gdpc import toolbox as TB
from gdpc import worldLoader as WL

def prep_land(WORLDSLICE, x1, z1, x2, z2, desired_y, base_block, height):
    """
    This function simply receives a rectangle and a desired y level, and places a rectangle of blocks there, 
    while clearing a number of blocks above specified by the height input. 

    Input:
        WORLDSLICE (object): The worldslice object of our build area
        x1 (int): Starting x point of our base rectangle.
        z1 (int): Starting z point of our base rectangle.
        x2 (int): Ending x point of our base rectangle.
        x2 (int): Ending z point of our base rectangle.
        desired_y (int): The y height of our base rectangle.
        base_block (string): The type of block we want as the base rectangle
        height (int): This value specifies how large the y value of our building is going to be.
    """
    heights = WORLDSLICE.heightmaps['MOTION_BLOCKING_NO_LEAVES']
    start_x, start_z, _, _ = WORLDSLICE.rect
    for z in range(z1, z2+1):
        for x in range(x1, x2+1):
            # Need to use local_x and local_z to index into height map
            local_x = x - start_x 
            local_z = z - start_z

            # Prints all heights for this chunk of land
            # print(f"({x}, {z}): {heights[(local_x, local_z)]}")

            INTF.placeBlock(x, desired_y, z, base_block)
    
    # Clear blocks above the desired y in our land chunk
    GEO.placeCuboid(x1, desired_y+1, z1, x2, desired_y+height, z2, 'air') 



# BELOW IS USED FOR TESTING
if __name__ == '__main__':
    STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.requestBuildArea()  # BUILDAREA
    # STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.setBuildArea(136, 63, 361, 179, 94, 417)
    print(f"Start x: {STARTX}")

    WORLDSLICE = WL.WorldSlice(STARTX, STARTZ, ENDX + 1, ENDZ + 1)
    prep_land(WORLDSLICE, 161, 394, 167, 401, 63, 'oak_planks', 20)


