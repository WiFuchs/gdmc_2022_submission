from gdpc import interface
from village_planner import VillagePlanner, BuildArea


if __name__ == '__main__':
    AROUND_PLAYER = True
    w = 256
    h = 256
    if AROUND_PLAYER:
        interface.runCommand("say start")
        resp = interface.runCommand(f"execute at @p run setbuildarea ~0 0 ~0 ~{w} 256 ~{h}")
        interface.runCommand("say end")

    sx, sy, sz, ex, ey, ez = interface.requestBuildArea()
    interface.runCommand(f"tp @a {sx} {256} {sz}")
    build_area = BuildArea(sx, sz, ex, ez)
    planner = VillagePlanner(build_area)
    planner.seed_buildings(goal_buildings=25)
