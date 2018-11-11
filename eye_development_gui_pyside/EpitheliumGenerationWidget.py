from PySide2 import QtCore
from PySide2 import QtWidgets

from eye_development_gui_pyside.SimulationWidget import SimulationWidget


class EpitheliumGenerationWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        ###################################################
        # epithelium display
        ###################################################
        self.epithelium_display = QtWidgets.QWidget()

        ###################################################
        # generation controls
        ###################################################
        ###
        # Generation action button placement
        ###
        self.generation_actions_button_group = QtWidgets.QButtonGroup()
        self.create_button = QtWidgets.QPushButton("Create")
        self.save_button = QtWidgets.QPushButton("Save")
        self.save_as_button = QtWidgets.QPushButton("Save As")
        self.load_button = QtWidgets.QPushButton("Load")
        self.generation_actions_button_group.addButton(self.create_button)
        self.generation_actions_button_group.addButton(self.save_button)
        self.generation_actions_button_group.addButton(self.save_as_button)
        self.generation_actions_button_group.addButton(self.load_button)
        ###
        # generation options
        ###
        # self.generation_options_widget = QtWidgets.QWidget()
        # self.min_cell_count_label = QtWidgets.QLabel("Min Cell Count")
        # self.min_cell_count_line_edit = QtWidgets.QLineEdit("100")
        # self.average_cell_size_label = QtWidgets.QLabel("Average Cell Size")
        # self.average_cell_size__line_edit = QtWidgets.QLineEdit("10")
        # self.cell_size_variance_label = QtWidgets.QLabel("Cell Size Variance")
        # self.cell_size_variance_line_edit = QtWidgets.QLineEdit("2")
        # generation_options_layout = QtWidgets.QGridLayout()
        # generation_options_layout.addWidget(self.min_cell_count_label, 0, 0)
        # generation_options_layout.addWidget(self.min_cell_count_line_edit, 0, 1)
        # generation_options_layout.addWidget(self.average_cell_size_label, 1, 0)
        # generation_options_layout.addWidget(self.average_cell_size__line_edit, 1, 1)
        # generation_options_layout.addWidget(self.cell_size_variance_label, 2, 0)
        # generation_options_layout.addWidget(self.cell_size_variance_line_edit, 2, 1)
        # self.generation_options_widget.setLayout(generation_options_layout)
        ###
        # combined generation controls
        ###
        self.generation_control_panel = QtWidgets.QWidget()
        generation_control_panel_layout = QtWidgets.QVBoxLayout()
        # generation_options_layout.addWidget(self.generation_actions_button_group)
        # generation_options_layout.addWidget(self.generation_options_widget)
        self.generation_control_panel.setLayout(generation_control_panel_layout)

        ###################################################
        # Combine control and display widgets
        ###################################################
        self.layout = QtWidgets.QHBoxLayout()
        #self.layout.addWidget(self.epithelium_display)
        self.layout.addWidget(self.generation_control_panel)
        self.setLayout(self.layout)


