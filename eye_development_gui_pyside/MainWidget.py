
from PySide2 import QtCore
from PySide2 import QtWidgets

from eye_development_gui_pyside.EpitheliumGenerationWidget import EpitheliumGenerationWidget
from epithelium_backend.SimulationController import SimulationController


class MainWidget(QtWidgets.QTabWidget):

    def __init__(self):
        """
        Initializes this
        """

        QtWidgets.QTabWidget.__init__(self)

        self.simulation_controller = SimulationController()  # type: SimulationController

        self.epithelium_generation_widget = EpitheliumGenerationWidget()  # type: EpitheliumGenerationWidget

        self.addTab(self.epithelium_generation_widget, "Epithelium Generation")
