from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui

from eye_development_gui_pyside.SimulationWidget import SimulationWidget


class EpitheliumGenerationWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        ###################################################
        # epithelium display
        ###################################################
        self.epithelium_display = QtWidgets.QWidget()
        self.epithelium_display.setMinimumSize(200, 200)
        self.epithelium_display.setAutoFillBackground(True)

        ###################################################
        # generation controls
        ###################################################
        ###
        # Generation action button placement
        ###
        self.create_button = QtWidgets.QPushButton("Create")
        self.save_button = QtWidgets.QPushButton("Save")
        self.save_as_button = QtWidgets.QPushButton("Save As")
        self.load_button = QtWidgets.QPushButton("Load")
        generation_actions_layout = QtWidgets.QHBoxLayout()
        generation_actions_layout.addWidget(self.create_button)
        generation_actions_layout.addWidget(self.save_button)
        generation_actions_layout.addWidget(self.save_as_button)
        generation_actions_layout.addWidget(self.load_button)
        ###
        # generation options
        ###
        self.min_cell_count_label = QtWidgets.QLabel("Min Cell Count")
        self.min_cell_count_line_edit = QtWidgets.QLineEdit("100")
        self.average_cell_size_label = QtWidgets.QLabel("Average Cell Size")
        self.average_cell_size__line_edit = QtWidgets.QLineEdit("10")
        self.cell_size_variance_label = QtWidgets.QLabel("Cell Size Variance")
        self.cell_size_variance_line_edit = QtWidgets.QLineEdit("2")
        generation_options_layout = QtWidgets.QGridLayout()
        generation_options_layout.addWidget(self.min_cell_count_label, 0, 0)
        generation_options_layout.addWidget(self.min_cell_count_line_edit, 0, 1)
        generation_options_layout.addWidget(self.average_cell_size_label, 1, 0)
        generation_options_layout.addWidget(self.average_cell_size__line_edit, 1, 1)
        generation_options_layout.addWidget(self.cell_size_variance_label, 2, 0)
        generation_options_layout.addWidget(self.cell_size_variance_line_edit, 2, 1)
        ###
        # combined generation controls
        ###
        self.generation_control_panel = QtWidgets.QWidget()
        generation_control_panel_layout = QtWidgets.QVBoxLayout()
        generation_control_panel_layout.addLayout(generation_actions_layout)
        generation_control_panel_layout.addLayout(generation_options_layout)
        generation_control_panel_layout.setAlignment(QtCore.Qt.TopEdge)
        self.generation_control_panel.setLayout(generation_control_panel_layout)
        self.generation_control_panel.setMaximumWidth(300)

        ###################################################
        # Combine control and display widgets
        ###################################################
        overall_layout = QtWidgets.QHBoxLayout()
        overall_layout.addWidget(self.epithelium_display)
        overall_layout.addWidget(self.generation_control_panel)
        self.setLayout(overall_layout)

    def on_create(self):
        pass