#! /usr/bin/python3

# === STRUCTURE #0
# These are technical values, you may ignore them or add them in your own files
__all__ = []
__author__ = "Blinkenlights"
__version__ = "v5.0"
__date__ = "17 February 2022"


# === STRUCTURE #1
# These are the modules (libraries) we will use in this code
# We are giving these modules shorter, but distinct, names for convenience
import random

from gdpc import geometry as GEO
from gdpc import interface as INTF
from gdpc import toolbox as TB
from gdpc import worldLoader as WL
import util.util as util
import structureLoader as loader
import lib.interfaceUtils as iu
import util.worldModification as worlModif

import json
from util.map import Map

# === STRUCTURE #2
# These variables are global and can be read from anywhere in the code
# I like to write them in capitals so I know they're global
# NOTE: if you want to change this value inside one of your functions,
#   you'll have to add a line of code. For an example search 'GLOBAL'

# Here we read start and end coordinates of our build area
# STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.requestBuildArea()  # BUILDAREA

# WORLDSLICE
# Using the start and end coordinates we are generating a world slice
# It contains all manner of information, including heightmaps and biomes
# For further information on what information it contains, see
#     https://minecraft.fandom.com/wiki/Chunk_format
#
# IMPORTANT: Keep in mind that a wold slice is a 'snapshot' of the world,
#   and any changes you make later on will not be reflected in the world slice
# WORLDSLICE = WL.WorldSlice(STARTX, STARTZ,
#                            ENDX + 1, ENDZ + 1)  # this takes a while


def buildTower(x, y, z, height=10, radius=10):

    print(f"Building tower at {x}, {z}...")


    #clear area
    GEO.placeCenteredCylinder(x, y, z, height, radius+1, "air")
    # lay the foundation
    GEO.placeCenteredCylinder(x, y, z, 1, radius+1, "oak_planks")

    # build ground floor
    GEO.placeCenteredCylinder(x, y + 1, z, 3, radius,
                              "oak_planks", tube=True)

    # extend height
   
    GEO.placeCenteredCylinder(
        x, y + 4, z, height, radius, "oak_planks", tube=True)
    height += 4

    # build roof
    GEO.placeCenteredCylinder(x, y + height, z, 1, radius, "oak_planks")
    GEO.placeCenteredCylinder(x, y + height + 1, z, 1,
                              radius - 1, "oak_planks")
    GEO.placeCenteredCylinder(x, y + height + 2, z, 1,
                              radius - 2, "oak_planks")
    GEO.placeCuboid(x, y + height, z, x, y + height
                    + 2, z, "glass")
    # INTF.placeBlock(x, y + 1, z, "beacon")

    # trim sides and add windows and doors
    GEO.placeCuboid(x + radius, y + 1, z, x + radius, y + height, z, "air")
    GEO.placeCuboid(x + radius - 1, y + 1, z,
                    x + radius - 1, y + height, z, "glass")
    # NOTE: When placing doors you need to place two blocks,
    #   the upper block defines the direction
    INTF.placeBlock(x + radius - 1, y + 1, z, "warped_door")
    INTF.placeBlock(x + radius - 1, y + 2, z,
                    "warped_door[facing=west, half=upper]")

    GEO.placeCuboid(x - radius, y + 1, z, x - radius, y + height + 2, z, "air")
    GEO.placeCuboid(x - radius + 1, y + 1, z,
                    x - radius + 1, y + height, z, "glass")
    INTF.placeBlock(x - radius + 1, y + 1, z, "warped_door")
    INTF.placeBlock(x - radius + 1, y + 2, z,
                    "warped_door[facing=east, half=upper]")

    GEO.placeCuboid(x, y + 1, z + radius, x, y + height , z + radius, "air")
    GEO.placeCuboid(x, y + 1, z + radius - 1,
                    x, y + height , z + radius - 1, "glass")
    INTF.placeBlock(x, y + 1, z + radius - 1, "warped_door")
    INTF.placeBlock(x, y + 2, z + radius - 1,
                    "warped_door[facing=south, half=upper]")

    GEO.placeCuboid(x, y + 1, z - radius, x, y + height , z - radius, "air")
    GEO.placeCuboid(x, y + 1, z - radius + 1,
                    x, y + height , z - radius + 1, "glass")
    INTF.placeBlock(x, y + 1, z - radius + 1, "warped_door")
    INTF.placeBlock(x, y + 2, z - radius + 1,
                    "warped_door[facing=north, half=upper]")



def buildStructure(x, z, radius, heightMap, referenceCoordinates, rotation, structures, biomesBlocks, worlModif):

    potentialStructs = []
    diameter = radius * 2
    for key in structures.keys():
        _, size = structures[key]
        if size[0] <= diameter and size[2] <= diameter:
            potentialStructs.append(key)
    
    chosenStruct = random.choice(potentialStructs)
    struct, size = structures[chosenStruct]

    xCoordinate = x + ((size[0]-2)//2) - 1
    zCoordinate = z + ((size[2]-2)//2) - 1
    yCoordinate = (heightMap[xCoordinate][zCoordinate] - 1)




    print("Building " + chosenStruct + " @ coordinates", xCoordinate, yCoordinate, zCoordinate)

    ## get biome 
    # biomeID = util.getNameBiome(util.getBiome(xCoordinate, zCoordinate, 10, 10))
    biomeID = util.getNameBiome(util.getBiome(referenceCoordinates[0] + xCoordinate, referenceCoordinates[2]  + zCoordinate, 10, 10))

    if str(biomeID) not in biomesBlocks:
        replacementBiomeBlocks = biomesBlocks["0"]
    else:
        replacementBiomeBlocks = biomesBlocks[str(biomeID)]

    


    struct.build([xCoordinate, -yCoordinate, zCoordinate], referenceCoordinates, rotation, worlModif, replacementBiomeBlocks)








if __name__ == '__main__':
    # NOTE: It is a good idea to keep this bit of the code as simple as
    #     possible so you can find mistakes more easily

    try:
        dx = 128
        dz = 128 

        INTF.runCommand("execute at @p run setbuildarea "f"~{-dx//2} 0 ~{-dz//2} ~{dx//2} 256 ~{dz//2}")

        STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.requestBuildArea()  # BUILDAREA

        interface = iu.Interface(buffering=True, caching = True)

        worlModif = worlModif.WorldModification(interface)


        WORLDSLICE = WL.WorldSlice(STARTX, STARTZ,
                           ENDX + 1, ENDZ + 1)
        
        heightMap = WORLDSLICE.heightmaps["MOTION_BLOCKING"]


        print("build area coordinates", STARTX, STARTZ, STARTY)

        referenceCoordinates = [STARTX, STARTY, STARTZ]

        structures = loader.loadAllResources()

        ## Load replacement biome blocks
        with open("data/biomeBlocks.json") as json_file:
            biomesBlocks = json.load(json_file)


        # get locally referenced build coordinates
        xloc =  1
        zloc =  1
        radius = 20
        height = 10
        rotation = 0 
        #rotation : No rotation = 0, rotation 90° = 1, rotation 180° = 2, rotation 270° = 3

        yCoordinate = heightMap[xloc][zloc] - 1

        buildTower(xloc + STARTX, yCoordinate, zloc + STARTZ, height=20, radius=1)

        
        buildStructure(xloc, zloc, radius, heightMap, referenceCoordinates, rotation, structures, biomesBlocks, worlModif)

        print("Done!")
    except KeyboardInterrupt:   # useful for aborting a run-away program
        print("Pressed Ctrl-C to kill program.")