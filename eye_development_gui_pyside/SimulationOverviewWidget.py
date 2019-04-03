from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui

from eye_development_gui_pyside.SimulationWidget import SimulationWidget


class SimulationOverviewWidget(QtWidgets.QWidget):
    """
    Allows for the setting of simulation options.
    """
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        ###########################################
        # Simulation
        ###########################################
        self.simulation_widget = SimulationWidget()

        #############################################
        # Simulation Options
        #############################################
        simulation_options_group_box = QtWidgets.QGroupBox("Simulation Options")
        simulation_options_group_box.setMaximumHeight(151)
        simulation_options_widget = QtWidgets.QWidget()
        simulation_options_scroll_area = QtWidgets.QScrollArea()
        simulation_options_layout = QtWidgets.QGridLayout()
        cell_max_size_label = QtWidgets.QLabel("Cell Max Size")
        self.cell_max_size_line_edit = QtWidgets.QLineEdit("25")
        cell_growth_rate_label = QtWidgets.QLabel("Cell Growth Rate")
        self.cell_growth_rate_line_edit = QtWidgets.QLineEdit("0.01")
        furrow_velocity_label = QtWidgets.QLabel("Furrow Velocity")
        self.furrow_velocity_line_edit = QtWidgets.QLineEdit("10")
        simulation_speed_label = QtWidgets.QLabel("Simulation Speed")
        self.simulation_speed_line_edit = QtWidgets.QLineEdit("10")
        simulation_options_layout.addWidget(cell_max_size_label, 0, 0)
        simulation_options_layout.addWidget(self.cell_max_size_line_edit, 0, 1)
        simulation_options_layout.addWidget(cell_growth_rate_label, 1, 0)
        simulation_options_layout.addWidget(self.cell_growth_rate_line_edit, 1, 1)
        simulation_options_layout.addWidget(furrow_velocity_label, 2, 0)
        simulation_options_layout.addWidget(self.furrow_velocity_line_edit, 2, 1)
        simulation_options_layout.addWidget(simulation_speed_label, 3, 0)
        simulation_options_layout.addWidget(self.simulation_speed_line_edit, 3, 1)
        simulation_options_widget.setLayout(simulation_options_layout)
        simulation_options_scroll_area.setWidget(simulation_options_widget)
        simulation_options_group_box_layout = QtWidgets.QHBoxLayout()
        simulation_options_group_box_layout.addWidget(simulation_options_scroll_area)
        simulation_options_group_box.setLayout(simulation_options_group_box_layout)

        #############################################
        # Specialization Options
        #############################################
        specialization_options_group_box = QtWidgets.QGroupBox("Specilization Options")
        specialization_options_widget = QtWidgets.QWidget()
        specialization_options_layout = QtWidgets.QFormLayout()
        specialization_options_scroll_area = QtWidgets.QScrollArea()
        # TODO: remove this -- add a bunch of things for testing
        for i in range(0, 10):
            label_name = "Specialization Option " + str(i)
            label = QtWidgets.QLabel(label_name)
            line_edit = QtWidgets.QLineEdit(str(i))
            specialization_options_layout.addWidget(label)
            specialization_options_layout.addWidget(line_edit)
        specialization_options_widget.setLayout(specialization_options_layout)
        specialization_options_scroll_area.setWidget(specialization_options_widget)
        specialization_options_group_box_layout = QtWidgets.QVBoxLayout()
        specialization_options_group_box_layout.addWidget(specialization_options_scroll_area)
        specialization_options_group_box.setLayout(specialization_options_group_box_layout)

        #############################################
        # Combined Options
        #############################################
        combined_options_widget = QtWidgets.QWidget()
        combined_options_layout = QtWidgets.QVBoxLayout()
        combined_options_layout.addWidget(simulation_options_group_box)
        combined_options_layout.addWidget(specialization_options_group_box)
        combined_options_widget.setLayout(combined_options_layout)
        combined_options_widget.setMaximumWidth(300)

        #############################################
        # Combined Options and Simulation
        #############################################
        overall_layout = QtWidgets.QHBoxLayout()
        overall_layout.addWidget(self.simulation_widget)
        overall_layout.addWidget(combined_options_widget)
        self.setLayout(overall_layout)

