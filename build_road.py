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

def build_road(WORLDSLICE, x1, z1, x2, z2, base_block):
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
 



# BELOW IS USED FOR TESTING
if __name__ == '__main__':
    # STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.requestBuildArea()  # BUILDAREA
    STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.setBuildArea(136, 50, 361, 179, 94, 417)
    print(f"Start x: {STARTX}")

    WORLDSLICE = WL.WorldSlice(STARTX, STARTZ, ENDX + 1, ENDZ + 1)
    build_road(WORLDSLICE, 146, 369, 156, 369, 'oak_planks')
    build_road(WORLDSLICE, 156, 369, 156, 389, 'oak_planks')
    

