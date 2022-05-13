import numpy as np
from gdpc.worldLoader import WorldSlice


class Map:
    """
    Map utility functions

    Copied from Tsukuba 2021:
        - calcClearHeightmap
    """

    @staticmethod
    def calc_clear_heightmap(world_slice: WorldSlice):
        """**Calculate a heightmap ideal for building**.

        Trees are ignored and water is considered ground.

        Args:
            worldSlice (WorldSlice): an instance of the WorldSlice class
                                     containing the raw heightmaps and block data

        Returns:
            any: numpy array containing the calculated heightmap
        """
        hm_mbnl = world_slice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
        heightmapNoTrees = hm_mbnl[:]
        area = world_slice.rect

        for x in range(area[2]):
            for z in range(area[3]):
                while True:
                    y = heightmapNoTrees[x, z]
                    block = world_slice.getBlockAt(
                        area[0] + x, y - 1, area[1] + z)
                    if block[-4:] == '_log':
                        heightmapNoTrees[x, z] -= 1
                    else:
                        break

        return np.array(np.minimum(hm_mbnl, heightmapNoTrees), dtype='uint8')

    @staticmethod
    def calc_flatness(build_area, sx: int, sz: int, ex: int, ez: int) -> int:
        """Evaluate flatness of a box on the heightmap heights. Flatness is the count of blocks that are not equal
        to the mode
        """
        heights = build_area.heightmap_no_trees
        flatness = 0
        value_counts = {}
        # create value counts for every height to find the mode
        for x in range(sx, ex + 1):
            for z in range(sz, ez + 1):
                cur_height = heights[(x, z)]

                # check for non-buildable blocks. If found, abort flatness search
                global_x, global_z = build_area.local_to_global(x, z)
                if build_area.worldslice.getBlockAt(global_x, cur_height-1, global_z) in ["minecraft:water", "minecraft:lava"]:
                    return -1

                if cur_height in value_counts:
                    value_counts[cur_height] += 1
                else:
                    value_counts[cur_height] = 1

        # calculate the total number of blocks that differ from the mode height
        mode_height = max(value_counts, key=value_counts.get)
        for height in value_counts:
            if height < mode_height:
                flatness += (mode_height - height) * value_counts[height]
            else:
                flatness += (height - mode_height) * value_counts[height]

        return flatness
