# from generation.structures.generated.generatedWell import GeneratedWell
# from generation.structures.generated.generatedQuarry import * 
from nbt import nbt
import json
from structures import *

STRUCTURE_PATH = "data/structures/"


def loadAllResources() : 
    # Loads structures

    def loadStructures(path, infoPath, name):
        nbtfile = nbt.NBTFile(STRUCTURE_PATH + path,'rb')
        with open(STRUCTURE_PATH + infoPath) as json_file:
           info = json.load(json_file)

        struct = Structures(nbtfile, info, name)
        structures[name] = (struct, [struct.file["size"][0].value, struct.file["size"][1].value, struct.file["size"][2].value])
        


    structures = {}

    print("Begin load ressources")
    loadStructures("houses/haybale/haybalehouse1.nbt", "houses/haybale/haybalehouse1.json", "haybalehouse1")
    loadStructures("houses/haybale/haybalehouse2.nbt", "houses/haybale/haybalehouse2.json", "haybalehouse2")
    loadStructures("houses/haybale/haybalehouse3.nbt", "houses/haybale/haybalehouse3.json", "haybalehouse3")
    loadStructures("houses/haybale/haybalehouse4.nbt", "houses/haybale/haybalehouse4.json", "haybalehouse4")

    loadStructures("houses/basic/basichouse1.nbt", "houses/basic/basichouse1.json", "basichouse1")
    loadStructures("houses/basic/basichouse2.nbt", "houses/basic/basichouse2.json", "basichouse2")
    loadStructures("houses/basic/basichouse3.nbt", "houses/basic/basichouse3.json", "basichouse3")


    loadStructures("houses/medium/mediumhouse1.nbt", "houses/medium/mediumhouse1.json", "mediumhouse1")
    loadStructures("houses/medium/mediumhouse2.nbt", "houses/medium/mediumhouse1.json", "mediumhouse2")
    loadStructures("houses/medium/mediumhouse3.nbt", "houses/medium/mediumhouse3.json", "mediumhouse3")

    loadStructures("houses/advanced/advancedhouse1.nbt", "houses/advanced/advancedhouse1.json", "advancedhouse1")

    loadStructures("functionals/lumberjachut/basiclumberjachut.nbt", "functionals/lumberjachut/basiclumberjachut.json", "basiclumberjachut")

    loadStructures("functionals/stonecutter/basicstonecutter.nbt", "functionals/stonecutter/basicstonecutter.json", "basicstonecutter")
    
    loadStructures("functionals/farm/basicfarm.nbt", "functionals/farm/basicfarm.json", "basicfarm")

    loadStructures("functionals/farm/mediumfarm1.nbt", "functionals/farm/mediumfarm1.json", "mediumfarm1")

    loadStructures("functionals/windmill/basicwindmill.nbt", "functionals/windmill/basicwindmill.json", "basicwindmill")
    loadStructures("functionals/windmill/mediumwindmill.nbt", "functionals/windmill/mediumwindmill.json", "mediumwindmill")

    loadStructures("functionals/furnace/basicfurnace1.nbt", "functionals/furnace/basicfurnace1.json", "basicfurnace1")

    loadStructures("functionals/smeltery/basicsmeltery.nbt", "functionals/smeltery/basicsmeltery.json", "basicsmeltery")

    loadStructures("functionals/workshop/basicworkshop.nbt", "functionals/workshop/basicworkshop.json", "basicworkshop")

    loadStructures("functionals/weaverhouse/basicweaverhouse.nbt", "functionals/weaverhouse/basicweaverhouse.json", "basicweaverhouse")


    loadStructures("representatives/townhall/basictownhall.nbt", "representatives/townhall/basictownhall.json", "basictownhall")

    loadStructures("representatives/jail/basicjail.nbt", "representatives/jail/basicjail.json", "basicjail")
    loadStructures("representatives/graveyard/basicgraveyard.nbt", "representatives/graveyard/basicgraveyard.json", "basicgraveyard")

    loadStructures("representatives/tavern/basictavern.nbt", "representatives/tavern/basictavern.json", "basictavern")
    loadStructures("representatives/barrack/basicbarrack.nbt", "representatives/barrack/basicbarrack.json", "basicbarrack")

    loadStructures("representatives/adventurerhouse/adventurerhouse.nbt", "representatives/adventurerhouse/adventurerhouse.json", "adventurerhouse")

    # addGeneratedStructures(GeneratedQuarry(), "functionals/quarry/basicgeneratedquarry.json", "basicgeneratedquarry")
    # addGeneratedStructures(GeneratedWell(), "representatives/well/basicgeneratedwell.json", "basicgeneratedwell")


    loadStructures("decorations/murderercache.nbt", "decorations/murderercache.json", "murderercache")

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


