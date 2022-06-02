# gdmc_2022_submission
GDMC 2022 submission, csc 570, Cal Poly SLO


## Introduction
 The goal of this project is to explore new algorithms in the lens of settlement creation in Minecraft, which entails designing an algorithm that can generate a lifelike settlement within a Minecraft map. We chose Minecraft since it offers one of the best sandbox environments to explore PCG within a game. Furthermore, there are several competitions that score PCG algorithms in Minecraft, providing us with metrics that can be used to evaluate how well the algorithm performs. Our goal is to implement an algorithm that can adapt to a certain landscape and produce a village that closely resembles something to real life. We plan to achieve this by studying previous implementations and build upon notable shortcomings like designing road connections and a practical village layout.
 
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

## Citation

## Contacts



[GDMC2021Tsukuba]: <https://github.com/MightyCode/GDMC2021Tsukuba>

[GDMC http interface]:  <https://github.com/nilsgawlik/gdmc_http_interface> 

[Forge Mod Launcher]: <https://files.minecraftforge.net/net/minecraftforge/forge/index_1.16.5.html>