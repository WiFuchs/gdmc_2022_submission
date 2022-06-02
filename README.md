# GDMC 2022 submission, CSC 570, Cal Poly SLO

Work done by WiFuchs, keonroohparvar, KamenShah, mlkrajewski

## Introduction
 The goal of this project is to explore new algorithms in the lens of settlement creation in Minecraft. This implementation focuses on structure placement, location of distinct building types and village connection mechanisms. Our goal was to improve upon previous works and furthermore achieve village layouts that are analogous to what could be seen in the world. While this work is domain specific to Minecraft, the frame of logic used in settlement creation may help improve procedural content generation used in other games. 

 
## Requirement
* python == 3.6
* x == 1.3.0
* x == 1.9
* minecraft version = 1.16.5
* [Forge Mod Launcher] (Download Recommended) 1.16.5 - 36.2.34
* [GDMC http interface]

## Components
* 1\. Generate building locations in an environment
* 2\. Deduce where distinct building types should be placed
* 3\. Build structures at building locations
* 4\. Connect village together with roads, bridges and tunnels


## Run Village Generation Script

* 1\. Install dependencies
    * a\. pip install -r requirements.txt
* 2\. Open minecraft launcher
* 3\. Ensure http interface @ http://localhost:9000/ is available
* 4\. Run python script
    * a\. python generate_village.py


## Attrubtion
Components are inspired by project [GDMC2021Tsukuba] . Thanks MightyCode, Harckyl, YusufSenel for your hard work!



[GDMC2021Tsukuba]: <https://github.com/MightyCode/GDMC2021Tsukuba>

[GDMC http interface]:  <https://github.com/nilsgawlik/gdmc_http_interface> 

[Forge Mod Launcher]: <https://files.minecraftforge.net/net/minecraftforge/forge/index_1.16.5.html>