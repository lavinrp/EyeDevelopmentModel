from PySide2 import QtWidgets
from PySide2 import QtGui


class SimulationWidget(QtWidgets.QWidget):
    """
    Displays an epithelium and controls its simulation
    """

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        #####
        # Simulation Controls
        #####
        simulation_controls_layout = QtWidgets.QHBoxLayout()
        self.simulation_start_button = QtWidgets.QPushButton("Start")
        self.simulation_pause_button = QtWidgets.QPushButton("Pause")
        self.simulation_stop_button = QtWidgets.QPushButton("Stop")
        simulation_controls_layout.addWidget(self.simulation_start_button)
        simulation_controls_layout.addWidget(self.simulation_pause_button)
        simulation_controls_layout.addWidget(self.simulation_stop_button)

        #####
        # Simulation Display
        #####
        self.epithelium_display = QtWidgets.QWidget()
        self.epithelium_display.setMinimumSize(200, 200)
        self.epithelium_display.setAutoFillBackground(True)

        #####################################
        # combine control and display widgets
        ######################################
        overall_layout = QtWidgets.QVBoxLayout()
        overall_layout.addLayout(simulation_controls_layout)
        overall_layout.addWidget(self.epithelium_display)
        self.setLayout(overall_layout)
