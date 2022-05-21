import os
import json 

# Class which serve to save all modification, do undo actions
class WorldModification: 
    DEBUG_MODE = False
    
    DEFAULT_PATH = "logs/"
    BLOCK_SEPARATOR = "$"
    PARTS_SEPARATOR = "°"
    

    def __init__(self, interface):
        self.interface = interface

        self.before_modification = []
        self.after_modificaton = []
        


    def setBlock(self, x, y, z, block, compareBlockState=False, placeImmediately=False):
        if WorldModification.DEBUG_MODE:
            previousBlock = self.interface.getBlock(x, y, z)

            # We won't replace block by same one, 
            # option to compare or not the state of both blocks -> [...]
            if block.split("[")[0] == previousBlock.split("[")[0]:
                if compareBlockState: 
                    pass
                    # TODO
                else :
                    return

            self.before_modification.append([x, y, z, previousBlock])
            self.after_modificaton.append([x, y, z, block])

        if placeImmediately : 
            self.interface.setBuffering(False)
            self.interface.setBlock(x, y, z, block)
            self.interface.setBuffering(True)
        else :
            self.interface.setBlock(x, y, z, block)

