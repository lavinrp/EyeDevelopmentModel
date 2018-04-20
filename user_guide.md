# Eye Development Model - User Guide
## Installation
1. [Download](https://www.python.org/downloads/) Python version 3.4 or greater
  * We recommend using a [virtual environment](https://docs.python.org/3/tutorial/venv.html). This is [easy](https://www.jetbrains.com/help/pycharm-edu/creating-virtual-environment.html) to do with IDEs like [pycharm](https://www.jetbrains.com/pycharm/)

2. Install required packages with [pip](https://docs.python.org/3/installing/). This is [easy](https://www.jetbrains.com/help/pycharm/installing-uninstalling-and-upgrading-packages.html) to do with IDEs like pycharm.
  * pyopengl - version 3.1.0 or greater
  * moderngl - version 5 or greater
  * numpy - version 1.13.3 or greater
  * pyrr - version 0.9.2 or greater
  * wxPython - version 4.0.1 or greater

3. [Clone](https://help.github.com/articles/cloning-a-repository/) or download the latest version of [Eye Development Model](https://github.uc.edu/lavinrp/EyeDevelopmentModel)
  * Most people should stay on the stable [master](https://github.uc.edu/lavinrp/EyeDevelopmentModel/tree/master) branch
  * Some brave souls may wish to use the unstable [develop](https://github.uc.edu/lavinrp/EyeDevelopmentModel/tree/develop) branch
___
## Settings
Eye Development Model currently only supports altering settings via environment variables.

The settings available are:
  * disable OpenGL core profile -> eye_develop_model_no_ogl_core
    * Forces Eye Development Model to use OpenGL in compatibility mode. Linux and Mac users should try setting this variable if they get a driver error that prevents epithelium rendering
    * On by default for Windows users
  * enable OpenGL core profile -> eye_develop_model_ogl_core
    * Forces Eye Development Model to Use OpenGL's Core Profile. Windows users should try settings this variable if they get a driver error that prevents epithelium rendering.
    * On by default for Linux and Mac users
  * Use legacy OpenGL display -> eye_develop_model_legacy_display
    * This forces Eye Development Model to use OpenGL imediate mode to do all of its rendering. This mode is **very** slow and minimally supported. It is advised that users only use this mode if they cannot render an epithelium using either of the two settings above
___
## General Use
### Getting an epithelium
An Epithelium can be generated or loaded from the _Epithelium Generation_ tab. After an epithelium is generated it can be saved for later use from this tab.
### Running a simulation
After selectin an epithelium you can simulate it via the _Simulation Overview_ and _Simulation_ tabs.
The _simulation Overview_ tab will let you start, stop and pause a simulation as well as change any of the simulations parameters, or any of the parameters used for cell specialization. The _Simulation_ tab will only let you start, pause, and stop the simulation, but it provides a better view.

Note that simulation and specialization options cannot be changed after a simulation has started.

___
## Changing the Code
### Custom Furrow Events
### Custom Cell Events
### Custom Rendering
