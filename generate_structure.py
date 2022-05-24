"""
This file serves as a file that places buildings based off of a list of building location seeds.

"""

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

def generate_structures(building_locations, heightMap, referenceCoordinates, rotation = 0):
    ## Load replacement biome blocks
    with open("data/biomeBlocks.json") as json_file:
        biomesBlocks = json.load(json_file)

    structures = loader.loadAllResources()


    iu_interface = iu.Interface(buffering=True, caching = True)
    worldModifier = worlModif.WorldModification(iu_interface)

    for xloc, zloc in building_locations:

        # yCoordinate = heightMap[xloc][zloc] - 1
        # buildTower(xloc + STARTX, yCoordinate, zloc + STARTZ, height=20, radius=1)


        buildStructure(xloc, zloc, 10, heightMap, referenceCoordinates, rotation, structures, biomesBlocks, worldModifier)
    

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

    xCoordinate = x - ((size[0]-2)//2) - 1
    zCoordinate = z - ((size[2]-2)//2) - 1
    yCoordinate = (heightMap[xCoordinate][zCoordinate] - 1)




    print("Building " + chosenStruct + " @ coordinates", xCoordinate, yCoordinate, zCoordinate)


    biomeID = util.getNameBiome(util.getBiome(referenceCoordinates[0] + xCoordinate, referenceCoordinates[2]  + zCoordinate, 10, 10))

    if str(biomeID) not in biomesBlocks:
        replacementBiomeBlocks = biomesBlocks["0"]
    else:
        replacementBiomeBlocks = biomesBlocks[str(biomeID)]

    


    struct.build([-xCoordinate, -yCoordinate, -zCoordinate], referenceCoordinates, rotation, worlModif, replacementBiomeBlocks)
   