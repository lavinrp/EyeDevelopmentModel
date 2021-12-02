<p align="right">
  <img src="./resources/EDM-1.png">
</p>

# Eye Development Model

## Introduction:
Eye Development Model (EDM) is a python application used to model and simulate the growth and development of eyes given different parameters.  The model is based mainly on what is known about the development of D. melanogaster eyes.  The user can observe in 2D what causes differentiation between different eye types by changing individual parameters of the cells.  The application is designed to also allow the user to define their own events to occur to on the epithelium of the eye.

<p align="center">
  <img src="./resources/developmentPathways.png">
</p>

## Starting EDM
Quick version:
1) [Download](https://www.python.org/downloads/) Python version 3.4 or greater
2) Install [PyCharm](https://www.jetbrains.com/pycharm/download/#section=windows)
3) If you opt to not use PyCharm,you will need to install dependencies with something like [pip](https://docs.python.org/3/installing/).:
   * pyopengl - version 3.1.0 or greater
   * moderngl - version 5 or greater
   * numpy - version 1.13.3 or greater
   * pyrr - version 0.9.2 or greater
   * wxPython - version 4.0.1 or greater
   >PyCharm uses requirements.txt to automatically get the needed packages. 
4) Clone this repo ```git clone https://github.com/lavinrp/EyeDevelopmentModel.git  ```
    >Tutorial of [clone](https://help.github.com/articles/cloning-a-repository/). Or download a zip of [Eye Development Model](https://github.com/lavinrp/EyeDevelopmentModel)
5) Open the project in PyCharm
6) After that everything should just work&trade; when you run main.py

For a more detailed description of how to get up and running, as well as how to use the application, see [this](user_guide.md).