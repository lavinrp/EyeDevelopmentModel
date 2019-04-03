from epithelium_backend.Epithelium import Epithelium
from epithelium_backend.ImportExport import import_epithelium
from epithelium_backend.ImportExport import export_epithelium
from epithelium_backend.ImportExport import import_simulation_settings
from epithelium_backend.ImportExport import export_simulation_settings

import sched


class SimulationController(object):
    """
    Stores and manipulates the state of entire simulation
    """

    def __init__(self):
        self.__active_epithelium = Epithelium(0)  # type: Epithelium
        self._simulating = False  # type: bool
        self._has_simulated = False  # type: bool

        # Track everything that needs to be notified when the
        # active epithelium is changed
        self.epithelium_listeners = []  # type: list

        # Track everything that can control the simulation of the active epithelium
        # (this is an observer of these objects)
        self.simulation_controllers = []  # type: list

        # TODO: register self as listener to simulation_controllers

        # TODO: establish camera listeners

        # timer for update loop
        self.update_timer = sched.scheduler()
        self.update_delay = 17  # type: int

        # save files
        self.active_epithelium_file = ""  # type: str
        self.active_simulation_settings_file = ""  # type: str
        self.temporary_epithelium_location = r"temp/temp_epithelium.epth"  # type: str

        # enable disable elements: state tracking
        self.generating_epithelium = False  # type: bool
        self.simulation_controllers_inputs_valid = True  # type: bool

    def on_update(self):

        # set update to update again
        self.update_timer.enter(self.update_delay, 1, self.on_update)



