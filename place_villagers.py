# Imports
from lib2to3.pytree import convert
from random import randint

import numpy as np

from gdpc import geometry as GEO
from gdpc import interface as INTF
from gdpc import toolbox as TB
from gdpc import worldLoader as WL
from util.encyclopedia import BuildingType

from helper_functions import convert_coords


def find_villager_info(struct):
    # print('Struct info: ')
    # print(struct.info)

    if 'villageInfo' not in struct.info.keys():
        print('No villager info')
        return 0, None
    

    village_dict = struct.info['villageInfo']
    num_people = village_dict['villager']
    if 'gameProfession' in village_dict.keys():
        return num_people, village_dict['gameProfession']
    return num_people, None

def spawnVillager(x, y, z, entity, profession):
    command = "summon " + entity + " " + str(x) + " " + str(y) + " " + str(z) + " "
    if profession is not None:
        command += "{VillagerData:{profession:" + profession +  "}" + "}"

    INTF.runCommand(command)


def place_villagers(struct, x, y, z):
    num_villagers, profession = find_villager_info(struct)
    print(f'Info for this building: {num_villagers}, {profession}')
    for i in range(num_villagers):
        spawnVillager(x, y, z, 'minecraft:villager', profession)

        print(f'Placing villager at {x},{y},{z}')

