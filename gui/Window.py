from tempfile import NamedTemporaryFile
from typing import List, Type
import pickle

from PyQt5 import QtCore, QtGui, QtWidgets, uic

from epithelium_backend.Epithelium import Epithelium
from epithelium_backend.FurrowEvent import FurrowEvent
from gui.workers import EpitheliumGenerator
from quick_change.FurrowEventList import furrow_event_list


class Window(QtWidgets.QMainWindow):
    """The main window of the application."""

    def __init__(self):
        super().__init__()

        self.ui = uic.loadUi('gui/resources/edm.ui', self)

        self.thread = QtCore.QThread(self)
        self.epithelium_generator = None

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_epithelium)

        self.epithelium_file = None
        self.simulation_file = None

        self.active_epithelium_widget = self.ui.epithelium_widget_1

        # Epithelium Generation Tab

        self.ui.create_epithelium_button.clicked.connect(self.create_epithelium)
        self.ui.save_epithelium_button.clicked.connect(self.save_epithelium)
        self.ui.save_as_epithelium_button.clicked.connect(self.save_as_epithelium)
        self.ui.load_epithelium_button.clicked.connect(self.load_epithelium)

        self.add_validator(self.ui.min_cell_count_input, int)
        self.add_validator(self.ui.average_cell_size_input, int)
        self.add_validator(self.ui.cell_variance_size_input, int)

        # Simulation Overview Tab

        self.ui.start_button_1.clicked.connect(self.start_simulation)
        self.ui.pause_button_1.clicked.connect(self.pause_simulation)
        self.ui.stop_button_1.clicked.connect(self.stop_simulation)

        self.add_validator(self.ui.cell_max_size_input, int)
        self.add_validator(self.ui.cell_growth_rate_input, float)
        self.add_validator(self.ui.furrow_velocity_input, int)
        self.add_validator(self.ui.simulation_speed_input, int)

        self.ui.save_simulation_button.clicked.connect(self.save_simulation)
        self.ui.save_as_simulation_button.clicked.connect(self.save_as_simulation)
        self.ui.load_simulation_button.clicked.connect(self.load_simulation)

        self.add_furrow_widgets()

        # Simulation Tab

        self.ui.start_button_2.clicked.connect(self.start_simulation)
        self.ui.pause_button_2.clicked.connect(self.pause_simulation)
        self.ui.stop_button_2.clicked.connect(self.stop_simulation)

        # Etc

        self.ui.tabs.currentChanged.connect(self.tab_changed)
        self.ui.generating_epithelium_label.hide()

    # Utility methods

    def add_validator(self, line_edit: QtWidgets.QLineEdit, data_type: Type):
        """
        Add a validator on to a line edit widget.
        :param line_edit: The widget to add the validator on
        :param data_type: The data type of the widget
        """
        line_edit.textChanged.connect(self.text_changed)

        # Regex for ints and floats, not needed for strings
        if data_type == int:
            regex = QtCore.QRegExp("[0-9]*")
        elif data_type == float:
            regex = QtCore.QRegExp("[0-9]+[.]?[0-9]*")
        else:
            return

        validator = QtGui.QRegExpValidator(regex, line_edit)
        line_edit.setValidator(validator)

    def add_furrow_widgets(self, events: List[FurrowEvent] = None):
        """
        Add custom furrow events to the specialization options area. By default, add the events from the quick_change
        module.
        :param events: Event list used when importing a simulation
        """
        if not events:
            try:
                events = self.active_epithelium_widget.epithelium.furrow.events
            except AttributeError:
                # Epithelium has not been created yet
                events = furrow_event_list

        layout = self.ui.specialization_options_content.layout()

        # Compare old and new furrow events
        new_labels = [event.name for event in events]
        for i in range(0, layout.count(), 2):
            widget = layout.itemAt(i).widget()
            if widget.text() not in new_labels:
                self.display_warning("Imported epithelium furrow events do not match your settings.")
                break

        # Remove old furrow events
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

        for event in events:
            label = QtWidgets.QLabel()
            label.setText(event.name)
            font = QtGui.QFont()
            font.setBold(True)
            label.setFont(font)

            self.ui.specialization_options_content.layout().addWidget(label)

            box = QtWidgets.QWidget()
            layout = QtWidgets.QGridLayout()

            for index, (key, value) in enumerate(event.field_types.items()):
                label = QtWidgets.QLabel()
                label.setText(key)
                layout.addWidget(label, index, 0)

                widget = QtWidgets.QLineEdit()
                widget.setText(str(value))
                # widget.setMaximumWidth(125)
                self.add_validator(widget, type(value))

                layout.addWidget(widget, index, 1)

            box.setLayout(layout)

            self.ui.specialization_options_content.layout().addWidget(box)

    def simulation_options_to_epithelium(self):
        """Apply the current simulation options to the epithelium."""
        cell_growth_rate = float(self.ui.cell_growth_rate_input.text())
        cell_max_size = int(self.ui.cell_max_size_input.text())

        for cell in self.active_epithelium_widget.epithelium.cells:
            cell.growth_rate = cell_growth_rate
            cell.max_radius = cell_max_size

        furrow_velocity = int(self.ui.furrow_velocity_input.text())
        self.active_epithelium_widget.epithelium.furrow.velocity = furrow_velocity

    def specialization_options_to_epithelium(self):
        """Apply the current specialization options to the epithelium."""
        # Prepare new values from fields
        options = {}
        layout = self.ui.specialization_options_content.layout()

        for i in range(0, layout.count(), 2):
            widget = layout.itemAt(i).widget()
            children = layout.itemAt(i+1).widget().children()
            temp = {}
            for j in range(1, len(children), 2):
                temp[children[j].text()] = children[j+1].text()
            options[widget.text()] = temp

        events = self.active_epithelium_widget.epithelium.furrow.events
        for event in events:
            for key, value in event.field_types.items():
                data_type = type(event.field_types[key])
                event.field_types[key] = data_type(options[event.name][key])

        self.active_epithelium_widget.epithelium.furrow.events = events

    def set_options_state(self, enabled: bool):
        """
        Set the state of simulation and specialization text field options.
        :param enabled: Enabled/disabled state
        """
        layout = self.ui.simulation_options.layout()

        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if isinstance(widget, QtWidgets.QLineEdit):
                widget.setEnabled(enabled)

        layout = self.ui.specialization_options_content.layout()

        for i in range(0, layout.count(), 2):
            children = layout.itemAt(i+1).widget().children()
            for j in range(len(children)):
                widget = children[j]
                if isinstance(widget, QtWidgets.QLineEdit):
                    widget.setEnabled(enabled)

    def import_epithelium(self, file_path: str = None):
        """
        Import an epithelium from a .epth file. If no file_path is specified, the current temporary file will be used
        or created.
        :param file_path: The path to the epithelium file
        """
        if not file_path:
            file_path = self.epithelium_file.name

        try:
            with open(file_path, "rb") as file:
                epithelium = pickle.load(file)
                self.active_epithelium_widget.epithelium = epithelium

        except (pickle.UnpicklingError, EOFError) as e:
            self.display_warning("Could not import epithelium from {}\n\n".format(file_path, e))

    def export_epithelium(self, file_path: str = None):
        """
        Export an epithelium to a .epth file. If no file_path is specified, the current temporary file will be used or
        created.
        :param file_path: The path to the epithelium file
        """
        epithelium = self.active_epithelium_widget.epithelium

        if not file_path:
            with NamedTemporaryFile(delete=False) as file:
                self.epithelium_file = file
                file_path = file.name

        with open(file_path, "wb") as file:
            pickle.dump(epithelium, file, protocol=pickle.HIGHEST_PROTOCOL)

    def import_simulation(self, file_path: str):
        """Import simulation settings from a .sim file."""
        try:
            with open(file_path, "rb") as file:
                simulation_options, furrow_events = pickle.load(file)

                self.ui.cell_max_size_input.setText(simulation_options["Cell Max Size"])
                self.ui.cell_growth_rate_input.setText(simulation_options["Cell Growth Rate"])
                self.ui.furrow_velocity_input.setText(simulation_options["Furrow Velocity"])
                self.ui.simulation_speed_input.setText(simulation_options["Simulation Speed"])

                self.add_furrow_widgets(furrow_events)

                self.simulation_file = file

        except (pickle.UnpicklingError, EOFError) as e:
            self.display_warning("Could not import simulation settings from {}\n\n{}".format(file_path, e))

    def export_simulation(self, file_path: str):
        """Export simulation settings to a .sim file."""
        simulation_options = {"Cell Max Size": self.ui.cell_max_size_input.text(),
                              "Cell Growth Rate": self.ui.cell_growth_rate_input.text(),
                              "Furrow Velocity": self.ui.furrow_velocity_input.text(),
                              "Simulation Speed": self.ui.simulation_speed_input.text()}

        if self.active_epithelium_widget.epithelium:
            events = self.active_epithelium_widget.epithelium.furrow.events
        else:
            events = furrow_event_list

        output = (simulation_options, events)

        with open(file_path, "wb") as file:
            pickle.dump(output, file, protocol=pickle.HIGHEST_PROTOCOL)
            self.simulation_file = file

    @staticmethod
    def display_warning(message: str):
        """
        Wrapper to display a warning box.
        :param message: The message to display
        """
        message_box = QtWidgets.QMessageBox()
        message_box.setText(message)
        message_box.setIcon(QtWidgets.QMessageBox.Warning)
        message_box.exec_()

    # Event Callbacks

    def tab_changed(self, index: int):
        """Listener for when the tab changes."""
        if index == 0:
            self.active_epithelium_widget = self.ui.epithelium_widget_1
        if index == 1:
            self.active_epithelium_widget = self.ui.epithelium_widget_2
        if index == 2:
            self.active_epithelium_widget = self.ui.epithelium_widget_3

    def text_changed(self):
        """
        Listener for when an input field changes. If a field becomes blank, the associated buttons will be disabled. If
        all fields become non-blank, the associated fields will be enabled.
        """
        if self.active_epithelium_widget == self.ui.epithelium_widget_1:
            if (self.ui.min_cell_count_input.text() == "" or self.ui.average_cell_size_input.text() == "" or
               self.ui.cell_variance_size_input.text() == ""):
                state = False
            else:
                state = True

            self.ui.create_epithelium_button.setEnabled(state)
            self.ui.save_epithelium_button.setEnabled(state)
            self.ui.save_as_epithelium_button.setEnabled(state)

        if self.active_epithelium_widget == self.ui.epithelium_widget_2:
            # Check if any of the furrow events are empty as well
            count = 0
            layout = self.ui.specialization_options_content.layout()
            for i in range(0, layout.count(), 2):
                widgets = layout.itemAt(i + 1).widget().children()
                for j in range(2, len(widgets), 2):
                    if widgets[j].text() == "":
                        count += 1

            if (self.ui.cell_max_size_input.text() == "" or self.ui.cell_growth_rate_input.text() == "" or
               self.ui.furrow_velocity_input.text() == "" or self.ui.simulation_speed_input.text() == "" or
               count > 0) or len(self.active_epithelium_widget.epithelium.cells) == 0:
                state = False
            else:
                state = True

            self.ui.start_button_1.setEnabled(state)
            self.ui.start_button_2.setEnabled(state)
            self.ui.pause_button_1.setEnabled(state)
            self.ui.pause_button_2.setEnabled(state)
            self.ui.stop_button_1.setEnabled(state)
            self.ui.stop_button_2.setEnabled(state)

    def keyPressEvent(self, e: QtGui.QKeyEvent):
        """
        Listener for when a key is pressed. When the enter key is pressed on the epithelium generation tab, a new
        epithelium is created. When the enter key is pressed on a simulation tab, the simulation is either started
        or stopped.
        """
        if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
            if self.active_epithelium_widget == self.ui.epithelium_widget_1:
                self.create_epithelium()
            else:
                if len(self.active_epithelium_widget.epithelium.cells) != 0:
                    if self.timer.isActive():
                        self.pause_simulation()
                    else:
                        self.start_simulation()

    @QtCore.pyqtSlot(Epithelium)
    def epithelium_callback(self, epithelium: Epithelium):
        """Callback for when the epithelium worker has completed generating an epithelium.
        :param epithelium: The new epithelium
        """
        self.active_epithelium_widget.epithelium = epithelium
        self.export_epithelium()
        self.thread.terminate()

        self.ui.generating_epithelium_label.hide()

        self.ui.start_button_1.setEnabled(True)
        self.ui.start_button_2.setEnabled(True)
        self.ui.pause_button_1.setEnabled(True)
        self.ui.pause_button_2.setEnabled(True)
        self.ui.stop_button_1.setEnabled(True)
        self.ui.stop_button_2.setEnabled(True)

    def update_epithelium(self):
        """Timer callback to update the epithelium widget."""
        self.active_epithelium_widget.epithelium.update()
        self.active_epithelium_widget.update()

    # Widget callbacks

    def create_epithelium(self):
        min_cell_count = int(self.ui.min_cell_count_input.text())
        average_cell_size = int(self.ui.average_cell_size_input.text())
        cell_variance_size = int(self.ui.cell_variance_size_input.text())

        self.epithelium_generator = EpitheliumGenerator(min_cell_count, average_cell_size, cell_variance_size)
        self.epithelium_generator.epithelium_signal.connect(self.epithelium_callback)
        self.epithelium_generator.moveToThread(self.thread)

        self.ui.generating_epithelium_label.show()

        self.thread.started.connect(self.epithelium_generator.generate_epithelium)
        self.thread.start()

    def save_epithelium(self):
        if isinstance(self.epithelium_file, NamedTemporaryFile):
            self.save_as_epithelium()
        else:
            self.export_epithelium(self.epithelium_file.name)

    def save_as_epithelium(self):
        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save", "", "Epithelium Files (*.epth)", options=options)

        if file_path:
            self.export_epithelium(file_path)

    def load_epithelium(self):
        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Load", "", "Epithelium Files (*.epth)", options=options)

        if file_path:
            self.epithelium_file = open(file_path, "rb")
            self.import_epithelium()

            epithelium = self.active_epithelium_widget.epithelium
            min_cell_count = len(epithelium.cells)

            try:
                if min_cell_count:
                    average_cell_size = round(sum(map(lambda cell: cell.radius, epithelium.cells)) / min_cell_count)
                else:
                    average_cell_size = 0
                cell_size_variance = round(max(map(lambda cell: abs(cell.radius - average_cell_size),
                                                   epithelium.cells)))
            except ValueError:  # Empty epithelium
                average_cell_size = 0
                cell_size_variance = 0

            self.ui.min_cell_count_input.setText(str(min_cell_count))
            self.ui.average_cell_size_input.setText(str(average_cell_size))
            self.ui.cell_variance_size_input.setText(str(cell_size_variance))

    def start_simulation(self):
        self.simulation_options_to_epithelium()
        self.specialization_options_to_epithelium()

        self.set_options_state(False)

        # Begin simulation timer
        fps = int(self.ui.simulation_speed_input.text())
        self.timer.start(1000//fps)

    def pause_simulation(self):
        self.timer.stop()

    def stop_simulation(self):
        self.timer.stop()
        self.set_options_state(True)

        # Reload the existing epithelium
        self.import_epithelium()

    def save_simulation(self):
        if self.simulation_file:
            self.export_simulation(self.simulation_file.name)
        else:
            self.save_as_simulation()

    def save_as_simulation(self):
        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save", "", "Simulation Files (*.sim)", options=options)

        if file_path:
            self.export_simulation(file_path)

    def load_simulation(self):
        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Load", "", "Simulation Files (*.sim)", options=options)

        if file_path:
            self.import_simulation(file_path)
