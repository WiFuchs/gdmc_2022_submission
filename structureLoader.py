# from generation.structures.generated.generatedWell import GeneratedWell
# from generation.structures.generated.generatedQuarry import * 
from nbt import nbt
import json
from structures import *

STRUCTURE_PATH = "data/structures/"


def loadAllResources() : 
    # Loads structures

    def loadStructures(path, infoPath, name, buildingType):
        nbtfile = nbt.NBTFile(STRUCTURE_PATH + path,'rb')
        with open(STRUCTURE_PATH + infoPath) as json_file:
           info = json.load(json_file)

        struct = Structures(nbtfile, info, name)
        if buildingType not in structures:
            structures[buildingType] = {}
        
        structures[buildingType][name] = (struct, [struct.file["size"][0].value, struct.file["size"][1].value, struct.file["size"][2].value])


    structures = {}

    print("Begin load ressources")
    
    # Haybale
    loadStructures("houses/haybale/haybalehouse1.nbt", "houses/haybale/haybalehouse1.json", "haybalehouse1", 'haybale')
    loadStructures("houses/haybale/haybalehouse2.nbt", "houses/haybale/haybalehouse2.json", "haybalehouse2", 'haybale' )
    loadStructures("houses/haybale/haybalehouse3.nbt", "houses/haybale/haybalehouse3.json", "haybalehouse3", 'haybale')
    loadStructures("houses/haybale/haybalehouse4.nbt", "houses/haybale/haybalehouse4.json", "haybalehouse4", 'haybale')

    # small house
    loadStructures("houses/basic/basichouse1.nbt", "houses/basic/basichouse1.json", "basichouse1", 'small_house')
    loadStructures("houses/basic/basichouse2.nbt", "houses/basic/basichouse2.json", "basichouse2", 'small_house')
    loadStructures("houses/basic/basichouse3.nbt", "houses/basic/basichouse3.json", "basichouse3", 'small_house')

    # Medium house
    loadStructures("houses/medium/mediumhouse1.nbt", "houses/medium/mediumhouse1.json", "mediumhouse1", 'medium_house')
    loadStructures("houses/medium/mediumhouse2.nbt", "houses/medium/mediumhouse1.json", "mediumhouse2", 'medium_house')
    loadStructures("houses/medium/mediumhouse3.nbt", "houses/medium/mediumhouse3.json", "mediumhouse3", 'medium_house')
    loadStructures("houses/advanced/advancedhouse1.nbt", "houses/advanced/advancedhouse1.json", "advancedhouse1", 'medium_house')

    # Farms
    loadStructures("functionals/farm/basicfarm.nbt", "functionals/farm/basicfarm.json", "basicfarm", 'farm')
    loadStructures("functionals/farm/mediumfarm1.nbt", "functionals/farm/mediumfarm1.json", "mediumfarm1", 'farm')


    # Misc
    loadStructures("functionals/lumberjachut/basiclumberjachut.nbt", "functionals/lumberjachut/basiclumberjachut.json", "basiclumberjachut", 'misc')
    loadStructures("functionals/stonecutter/basicstonecutter.nbt", "functionals/stonecutter/basicstonecutter.json", "basicstonecutter", 'misc')
    loadStructures("functionals/furnace/basicfurnace1.nbt", "functionals/furnace/basicfurnace1.json", "basicfurnace1", 'misc')
    loadStructures("functionals/smeltery/basicsmeltery.nbt", "functionals/smeltery/basicsmeltery.json", "basicsmeltery", 'misc')
    loadStructures("functionals/workshop/basicworkshop.nbt", "functionals/workshop/basicworkshop.json", "basicworkshop", 'misc')
    loadStructures("functionals/weaverhouse/basicweaverhouse.nbt", "functionals/weaverhouse/basicweaverhouse.json", "basicweaverhouse", 'misc')   


    # Windmill
    loadStructures("functionals/windmill/basicwindmill.nbt", "functionals/windmill/basicwindmill.json", "basicwindmill", 'windmill')
    loadStructures("functionals/windmill/mediumwindmill.nbt", "functionals/windmill/mediumwindmill.json", "mediumwindmill", 'windmill')

    
    # Townhall
    loadStructures("representatives/townhall/basictownhall.nbt", "representatives/townhall/basictownhall.json", "basictownhall", 'townhall')

    # Graveyard
    loadStructures("representatives/graveyard/basicgraveyard.nbt", "representatives/graveyard/basicgraveyard.json", "basicgraveyard", 'graveyard')

    # Tavern
    loadStructures("representatives/tavern/basictavern.nbt", "representatives/tavern/basictavern.json", "basictavern", 'tavern')


    # Enforcement
    # loadStructures("representatives/adventurerhouse/adventurerhouse.nbt", "representatives/adventurerhouse/adventurerhouse.json", "adventurerhouse", 'adventure')
    loadStructures("representatives/jail/basicjail.nbt", "representatives/jail/basicjail.json", "basicjail", 'enforcement')
    loadStructures("representatives/barrack/basicbarrack.nbt", "representatives/barrack/basicbarrack.json", "basicbarrack", 'enforcement')

    # addGeneratedStructures(GeneratedQuarry(), "functionals/quarry/basicgeneratedquarry.json", "basicgeneratedquarry")
    # addGeneratedStructures(GeneratedWell(), "representatives/well/basicgeneratedwell.json", "basicgeneratedwell")


    # loadStructures("decorations/murderercache.nbt", "decorations/murderercache.json", "murderercache")

    # Load lootTable
    # loadLootTable("houses/kitchenhouse.json", "kitchenhouse")
    # loadLootTable("houses/bedroomhouse.json", "bedroomhouse")

    # loadLootTable("functionals/windmill.json", "windmill")
    # loadLootTable("functionals/basiclumberjachut.json", "basiclumberjachut")
    # loadLootTable("functionals/basicfarm.json", "basicfarm")
    # loadLootTable("functionals/basicstonecutter.json", "basicstonecutter")
    # loadLootTable("functionals/smeltery.json", "smeltery")
    # loadLootTable("functionals/workshop.json", "workshop")

    # loadLootTable("representatives/townhall.json", "townhall")
    # loadLootTable("representatives/jail.json", "jail")
    # loadLootTable("representatives/tavern.json", "tavern")
    # loadLootTable("representatives/barrack.json", "barrack")

    # loadLootTable("representatives/adventurerhouse.json", "adventurerhouse")

    # loadLootTable("decorations/murderercache.json", "murderercache")

    print("End load ressources")


    return structures


