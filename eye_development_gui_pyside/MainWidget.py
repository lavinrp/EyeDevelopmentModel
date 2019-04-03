
from PySide2 import QtCore
from PySide2 import QtWidgets

from eye_development_gui_pyside.EpitheliumGenerationWidget import EpitheliumGenerationWidget
from eye_development_gui_pyside.SimulationWidget import SimulationWidget
from eye_development_gui_pyside.SimulationOverviewWidget import SimulationOverviewWidget
from epithelium_backend.SimulationController import SimulationController


class MainWidget(QtWidgets.QTabWidget):

    def __init__(self):
        """
        Initializes this
        """

        QtWidgets.QTabWidget.__init__(self)

        # MVC control
        self.simulation_controller = SimulationController()  # type: SimulationController

        # tab widgets
        self.epithelium_generation_widget = EpitheliumGenerationWidget()  # type: EpitheliumGenerationWidget
        self.simulation_overview_widget = SimulationOverviewWidget()  # type: SimulationOverviewWidget
        self.simulation_widget = SimulationWidget()  # type: SimulationWidget

        # tabs
        self.addTab(self.epithelium_generation_widget, "Epithelium Generation")
        self.addTab(self.simulation_overview_widget, "Simulation Overview")
        self.addTab(self.simulation_widget, "Simulation")

        # sizing
        self.setMinimumSize(500, 300)
