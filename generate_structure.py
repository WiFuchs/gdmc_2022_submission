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

def generate_structures(building_locations, heightMap, referenceCoordinates):
    """
    Builds a building at all building locations using building specifications

    :param building_locations: List of building specs
    :param heightMap: Grid map of heights in Building Area   
    :param referenceCoordinates: Coordinates of Building Area   
    """
    ## Load replacement biome blocks
    with open("data/biomeBlocks.json") as json_file:
        biomesBlocks = json.load(json_file)

    # Load in all structures
    structures = loader.loadAllResources()

    # Instantiate modifier API (puts blocks in world)
    iu_interface = iu.Interface(buffering=True, caching = True)
    worldModifier = worlModif.WorldModification(iu_interface)

    # Build structure at every building location using building specs
    for building in building_locations:
        buildStructure(building, heightMap, referenceCoordinates, structures, biomesBlocks, worldModifier)



def buildStructure(building, heightMap, referenceCoordinates, structures, biomesBlocks, worlModif):
    """
    Builds an individual building based off building type

    :param building: Building specifications 
    :param heightMap: Grid map of heights in Building Area   
    :param referenceCoordinates: Coordinates of Building Area   
    :param structures: Coordinates of Building Area   
    :param biomesBlocks: Dictionary of blocks that should be used based off the biome
    :param worlModif: API that puts blocks at specific coordinates   
    """

    # Choose a random structure with building_type
    buildingTypeName = building.building_type.name
    potentialStructs = list(structures[buildingTypeName].keys())
    chosenStruct = random.choice(potentialStructs)

    # Get building coordinates
    struct, size = structures[buildingTypeName][chosenStruct]
    xCoordinate = building.x - ((size[0]-2)//2) - 1
    zCoordinate = building.z - ((size[2]-2)//2) - 1
    yCoordinate = (heightMap[xCoordinate][zCoordinate] - 1)
    # yCoordinate = building.y



    print("Building " + chosenStruct + " @ coordinates", xCoordinate, yCoordinate, zCoordinate)


    # Infer the biome in which the structure will be placed
    biomeID = util.getNameBiome(util.getBiome(referenceCoordinates[0] + xCoordinate, referenceCoordinates[2]  + zCoordinate, 10, 10))
    if str(biomeID) not in biomesBlocks:
        replacementBiomeBlocks = biomesBlocks["0"]
    else:
        replacementBiomeBlocks = biomesBlocks[str(biomeID)]

    
    # Build structure
    struct.build([-xCoordinate, -yCoordinate, -zCoordinate], referenceCoordinates, building.rotation, worlModif, replacementBiomeBlocks)
   
