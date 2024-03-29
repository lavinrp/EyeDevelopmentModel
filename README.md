<p align="center">
  <img src="./resources/EDM-1.png" width="200px" height="200px">
</p>

# Eye Development Model

## Introduction:
Eye Development Model (EDM) is a python application used to model and simulate the growth and development of eyes given different parameters.  The model is based mainly on what is known about the development of D. melanogaster eyes.  The user can observe in 2D what causes differentiation between different eye types by changing individual parameters of the cells.  The application is designed to also allow the user to define their own events to occur to on the epithelium of the eye.

<p align="center">
  <img src="./resources/developmentPathways.png">
</p>

## Starting EDM
Quick version:
1) [Download](https://www.python.org/downloads/) Python version 3.7 or greater
2) Install [PyCharm](https://www.jetbrains.com/pycharm/download/#section=windows).  If you opt to _not_ use PyCharm, you will need to install dependencies with something like [pip](https://docs.python.org/3/installing/).:
   * pyopengl - version 3.1.0
   * moderngl - version 5.5.3
   * numpy - version 1.17.2
   * pyrr - version 0.10.3
   * wxPython - version 4.0.6
   >PyCharm uses requirements.txt to automatically get the needed packages. 
3) Get EDM with [git clone](https://help.github.com/articles/cloning-a-repository/). Or download a zip of [Eye Development Model](https://github.com/buschbeck-lab/EyeDevelopmentModel/archive/refs/heads/master.zip)
   
   `git clone https://github.com/buschbeck-lab/EyeDevelopmentModel.git`
4) Open the project in PyCharm
5) Run main.py

For a more detailed description of how to get up and running see [this user guide](user_guide.md).

## General Use
### Epithelium Generation
An Epithelium can be generated or loaded from the _Epithelium Generation_ tab in the top left. After an epithelium is generated it can be saved to be loaded later or sent to someone else to load.
<p align="center">
  <img src="./resources/EpitheliumGenerationTab.png">
</p>

### Simulation Overview
The _simulation Overview_ tab will let you start, stop, and pause a simulation as well as change any of the simulation's parameters, or any of the parameters used for cell specialization.
<p align="center">
  <img src="./resources/SimOverviewTab.PNG">
</p>

### Simulation
The _Simulation_ tab will only let you start, pause, and stop the simulation, but it provides a better view.
<p align="center">
  <img src="./resources/SimulationTab.PNG">
</p>

## Reporting Bugs
Please report any and all bugs to the [GitHub Issue Tracker](https://github.com/buschbeck-lab/EyeDevelopmentModel/issues)