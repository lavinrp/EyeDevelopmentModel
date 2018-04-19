"""Subclass of MainFrameBase, which is generated by wxFormBuilder."""

from epithelium_backend.CellFactory import CellFactory
from epithelium_backend.Epithelium import Epithelium
from epithelium_backend.ImportExport import import_epithelium
from epithelium_backend.ImportExport import export_epithelium
from epithelium_backend.ImportExport import import_simulation_settings
from epithelium_backend.ImportExport import export_simulation_settings
from quick_change.FurrowEventList import furrow_event_list
from eye_development_gui.FieldType import FieldType
from eye_development_gui.eye_development_gui import MainFrameBase

from eye_development_gui.background_workers.EpitheliumGenerationWorker import EpitheliumGenerationEvent
from eye_development_gui.background_workers.EpitheliumGenerationWorker import EpitheliumGenerationWorker
from eye_development_gui.background_workers.EpitheliumGenerationWorker import EVT_GENERATE_EPITHELIUM

import wx
import wx.xrc
from wx.core import TextCtrl
from wx.core import FileDialog
from wx.core import StaticText
from wx.core import Button


# Implementing MainFrameBase
class MainFrame(MainFrameBase):
    """Wx frame that contains the entire gui.
     Also acts as both the model and the control for the GUI."""

    def __init__(self, parent):
        """Initializes the GUI and all the data of the model."""
        MainFrameBase.__init__(self, parent)

        self.status_bar = self.CreateStatusBar()  # type: wx.StatusBar
        self.init_icon()

        self.Bind(wx.EVT_CLOSE, self.on_close)

        MainFrame.add_fields(self.m_sim_overview_spec_options_scrolled_window, furrow_event_list)

        self.__active_epithelium = Epithelium(0)  # type: Epithelium
        self._simulating = False
        self._has_simulated = False

        # Track all the panels that need to be notified when the
        # active epithelium is changed
        self.epithelium_listeners = [self.m_epithelium_gen_display_panel,
                                     self.m_sim_overview_display_panel,
                                     self.m_simulation_display_panel]  # type: list

        # Track panels that can control the simulation of the active epithelium
        # (this is an observer of these objects)
        self.simulation_controllers = [self.m_sim_overview_display_panel,
                                       self.m_simulation_display_panel]  # type: list
        for controller in self.simulation_controllers:
            controller.simulation_listeners.append(self)

        # establish camera listeners
        sim_canvas = self.m_simulation_display_panel.m_epithelium_display.gl_canvas
        overview_canvas = self.m_sim_overview_display_panel.m_epithelium_display.gl_canvas
        generation_canvas = self.m_epithelium_gen_display_panel.gl_canvas
        sim_canvas.camera_listeners.extend((overview_canvas, generation_canvas))
        overview_canvas.camera_listeners.extend((sim_canvas, generation_canvas))
        generation_canvas.camera_listeners.extend((sim_canvas, overview_canvas))

        # Timer for updating the epithelium
        self.simulation_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_epithelium, self.simulation_timer)

        # save files
        self.active_epithelium_file = ""
        self.active_simulation_settings_file = ""
        self.temporary_epithelium_location = r"temp/temp_epithelium.epth"

        # enable disable elements: state tracking
        self.generating_epithelium = False  # type: bool
        self.simulation_controllers_inputs_valid = True  # type: bool
        self.update_enabled_widgets()

        # worker thread

        self.Bind(EVT_GENERATE_EPITHELIUM, self.on_epithelium_generated)

    # region dynamic input creation

    @staticmethod
    def create_callback(field_type: FieldType, text_control: wx.TextCtrl):
        """
        Create a callback that validates/sets the field type's value
        when the text_control's input changes.
        """
        def callback(event):
            # If valid, sets the value to it and returns True. Otherwise returns False.
            field_type.validate(text_control.GetLineText(0))
            event.Skip()
        return callback

    @staticmethod
    def add_fields(window: wx.Window, events: list):
        """
        Dynamically generate input fields from the furrow events.

        :param window: the wxform window to add the inputs to.
        :param events: a list of furrow events to generate gui inputs from.
        """
        # This was copied from the dynamically generated code that wxFormBuilder spits out.
        # I don't totally understand it.
        g_sizer = wx.GridSizer(0, 2, 0, 0)
        for event in events:
            for param_name, field_type in event.field_types.items():
                # The left hand side -- the label of the input
                static_text = wx.StaticText(window, wx.ID_ANY, param_name, wx.DefaultPosition, wx.DefaultSize, 0)
                static_text.Wrap(-1)
                g_sizer.Add(static_text, 0, wx.ALL, 5)
                # The right hand side -- the input box
                text_control =  wx.TextCtrl(window , wx.ID_ANY, str(field_type.value), wx.DefaultPosition, wx.DefaultSize, 0 )
                # Bind the input box to the field_type value
                text_control.Bind(wx.EVT_TEXT, MainFrame.create_callback(field_type, text_control))
                g_sizer.Add(text_control, 0, wx.ALL, 5)
        window.SetSizer(g_sizer)
        window.Layout()
        g_sizer.Fit(window)

    # endregion dynamic input creation

    # region general event handling

    def ep_gen_create_callback(self, event):
        """
        Callback for ep_gen_create_button. Attempts to create a
        new epithelium from the epithelium generation inputs
        and sets it as the active epithelium. If creation fails the
        user is notified of the invalid parameters.

        Pauses any ongoing simulations.
        """

        # pause any ongoing simulations
        self.simulating = False

        # validate inputs
        if self.ep_gen_input_validation():

            # convert inputs to usable value

            # min cell count
            min_cell_count_str = self.str_from_text_input(self.min_cell_count_text_ctrl)  # type: str
            min_cell_count = int(min_cell_count_str)  # type: int

            # avg cell size
            avg_cell_size_str = self.str_from_text_input(self.avg_cell_size_text_ctrl)  # type: str
            avg_cell_size = float(avg_cell_size_str)

            # cell size variance
            cell_size_variance_str = self.str_from_text_input(self.cell_size_variance_text_ctrl)  # type: str
            cell_size_variance = float(cell_size_variance_str)

            # create active epithelium in the background
            worker = EpitheliumGenerationWorker(self,
                                                min_cell_count,
                                                avg_cell_size,
                                                radius_divergence=cell_size_variance / avg_cell_size)
            worker.setDaemon(True)
            self.generating_epithelium = True
            self.update_enabled_widgets()
            worker.start()

    def on_close(self, event: wx.CloseEvent):
        """Callback invoked when closing the application.
        Halts simulation then allows the default close handler to exit the application."""
        self.simulating = False
        event.Skip()

    def on_ep_gen_user_input(self, event: wx.Event):
        """
        Callback invoked whenever a user alters an epithelium generation input.
        Validates all epithelium generation options.
        :param event: event generated by the user input
        """
        self.ep_gen_input_validation()
        event.Skip()

    def on_epithelium_save(self, event: wx.Event):
        """
        Callback invoked whenever a user saves an epithelium (via save or save as).
        Saves the active epithelium to the active epithelium file.
        :param event: event generated by user input
        """

        # if no active file run a save as instead
        if not self.active_epithelium_file:
            self.on_epithelium_save_as(event)
            return

        # attempt to save to active file
        export_epithelium(self.active_epithelium, self.active_epithelium_file)

        # do not consume event
        event.Skip(False)

    def on_epithelium_save_as(self, event: wx.Event):
        """
        Callback that is invoked whenever a user clicks the save as button, or clicks the save button
        without a selected file.
        Selects an active file then saves the active epithelium to that file.
        :param event: event generated by user input.
        """

        # find new file name
        save_as_dialog = FileDialog(self, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        save_as_dialog.Show()
        if save_as_dialog.ShowModal() == wx.ID_CANCEL:
            return  # the user changed their mind
        self.active_epithelium_file = save_as_dialog.GetFilename()

        # save to new file name
        self.on_epithelium_save(event)

    def on_epithelium_load(self, event: wx.Event):
        """
        Callback that is invoked whenever a user clicks the epithelium generation load button.
        Creates an epithelium from an epithelium save file and sets the new epithelium to
        be the active epithelium. The selected file becomes the active file. Updates the gui
        to match the values of the new active epithelium.
        :param event:
        :return:
        """
        load_dialog = FileDialog(self, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        load_dialog.Show()
        if load_dialog.ShowModal() == wx.ID_CANCEL:
            return  # the user changed their mind

        # load the file
        active_epithelium_file = load_dialog.GetFilename()
        imported_epithelium = import_epithelium(active_epithelium_file)
        if imported_epithelium:

            # check if the furrow events of the imported epithelium match the local furrow events
            furrow_events_match = True
            for i in range(len(furrow_event_list)):
                if imported_epithelium.furrow.events[i].name != furrow_event_list[i].name:
                    furrow_events_match = False
                    break

            if not furrow_events_match:
                # warn that different furrow events may lead to different results
                dlg = wx.MessageDialog(self, "Furrow Events Don't Match",
                                       "The furrow_event_list paired with the loaded epithelium does not match the"
                                       "local furrow event list. This may impact simulation results.",
                                       wx.OK | wx.ICON_WARNING)
                dlg.ShowModal()
                dlg.Destroy()

            # update epithelium
            self.active_epithelium_file = active_epithelium_file
            self.active_epithelium = imported_epithelium
            # update gui
            self.update_gui_to_active_epithelium()

        else:
            dlg = wx.MessageDialog(self, "Could not load epithelium!", "Unable To Load", wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()

        # do not consume event
        event.Skip(False)

    def on_sim_overview_save(self, event: wx.Event):
        """
        Callback invoked whenever a user saves simulation options (via save or save as).
        Saves the simulation options to the active simulation options file.
        :param event: event generated by user input
        """

        # if no active file run a save as instead
        if not self.active_simulation_settings_file:
            self.on_sim_overview_save_as(event)
            return

        # attempt to save to active file
        export_simulation_settings(list(self.m_sim_overview_sim_options_scrolled_window.GetChildren()),
                                   furrow_event_list,
                                   self.active_simulation_settings_file)

        # do not consume event
        event.Skip(False)

    def on_sim_overview_save_as(self, event: wx.Event):
        """
        Callback that is invoked whenever a user clicks the save as button for simulation options,
        or clicks the save button for simulation options without a selected file.
        Selects an active file then saves the simulation options to that file.
        :param event: event generated by user input.
        """

        # find new file name
        save_as_dialog = FileDialog(self, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        save_as_dialog.Show()
        if save_as_dialog.ShowModal() == wx.ID_CANCEL:
            return  # the user changed their mind
        self.active_simulation_settings_file = save_as_dialog.GetFilename()

        # save to new file name
        self.on_sim_overview_save(event)

    def on_sim_overview_load(self, event: wx.Event):
        """
        Callback that is invoked whenever a user clicks the simulation options load button.
        Loads simulation options from the simulation options save file. The selected file
        becomes the active file. Updates the gui to match the new values.
        to match the new values.
        :return:
        """
        load_dialog = FileDialog(self, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        load_dialog.Show()
        if load_dialog.ShowModal() == wx.ID_CANCEL:
            return  # the user changed their mind

        # load the file
        active_simulation_settings_file = load_dialog.GetFilename()
        imported_settings = import_simulation_settings(active_simulation_settings_file)

        # update with values from loaded file
        if imported_settings:
            self.active_simulation_settings_file = active_simulation_settings_file
            simulation_scroll_children = self.m_sim_overview_sim_options_scrolled_window.GetChildren()
            for i in range(len(simulation_scroll_children)):
                if isinstance(simulation_scroll_children[i], wx.StaticText):
                    static_text = simulation_scroll_children[i]  # type: wx.StaticText
                    text_ctrl = simulation_scroll_children[i + 1]  # type: TextCtrl
                    text_ctrl.SetValue(imported_settings[static_text.GetLabelText()])

            self.m_sim_overview_spec_options_scrolled_window.DestroyChildren()
            self.add_fields(self.m_sim_overview_spec_options_scrolled_window, furrow_event_list)

        else:
            dlg = wx.MessageDialog(self,
                                   "Could not load simulation Settings!",
                                   "Unable To Load",
                                   wx.OK | wx.ICON_WARNING)
            dlg.ShowModal()
            dlg.Destroy()

        # do not consume event
        event.Skip(False)

    def on_sim_overview_user_input(self, event: wx.Event):
        """
        Callback invoked whenever a user alters a simulation input in the simulation overview tab.
        Validates all simulation paramaters.
        :param event: event generated by user input.
        """
        self.sim_overview_input_validation()
        event.Skip()

    def on_size(self, event: wx.Event):
        """
        Callback function invoked when the application is resized. Helps sizers maintain correct spacing.
        :param event: Resize event.
        """

        # resize scrolled windows for settings in simulation overview
        cell_option_count = int(len(self.m_sim_overview_sim_options_scrolled_window.GetChildren()) / 2)
        space_per_cell_child = 60
        self.m_sim_overview_sim_options_scrolled_window.SetMinSize(
            (self.m_sim_overview_sim_options_scrolled_window.GetMinWidth(),
             min(cell_option_count * space_per_cell_child, self.GetSize().height / 5)))
        event.Skip()

    def on_simulation_stopped(self):
        """
        Function called when the simulation of an epithelium should fully stop (not just pause).
        Resets the epithelium to its pre-simulation state.
        """
        imported_epithelium = import_epithelium(self.temporary_epithelium_location)
        if imported_epithelium:
            self.active_epithelium = imported_epithelium

    # endregion event handling

    # region background workers

    def on_epithelium_generated(self, event: EpitheliumGenerationEvent):
        """
        Callback invoked after a background worker has finished creating an epithelium.
        :param event: Event containing the produced epithelium.
        :return:
        """
        self.active_epithelium = event.get_epithelium()
        self.generating_epithelium = False
        self.update_enabled_widgets()

    # endregion background workers

    # region input validation

    def ep_gen_input_validation(self) -> bool:
        """validates all epithelium generation inputs
        :return: rue if all inputs validate. False otherwise.
        """

        # have to calculate and return values separately to avoid short circuiting the validation
        avg_cell_size = self.validate_ep_gen_avg_cell_size()
        variance = self.validate_ep_gen_cell_size_variance()
        cell_count = self.validate_ep_gen_min_cell_count()
        return avg_cell_size and variance and cell_count

    def sim_overview_input_validation(self) -> bool:
        """Validates all simulation overview simulation inputs.
        :return: True if all inputs validate. False otherwise.
        """
        furrow_velocity = self.validate_ep_gen_furrow_velocity()
        cell_max_size = self.validate_ep_gen_cell_max_size()
        cell_growth_rate = self.validate_ep_gen_cell_growth_rate()
        sim_speed = self.validate_simulation_speed()

        inputs_valid = furrow_velocity and cell_max_size and cell_growth_rate and sim_speed
        self.simulation_controllers_inputs_valid = inputs_valid

        self.update_enabled_widgets()

        return inputs_valid

    def validate_ep_gen_min_cell_count(self) -> bool:
        """Validates user input to min_cell_count_text_ctrl
        :return: Return True if the validation was successful. Return False otherwise.
        """
        min_cell_count_str = self.str_from_text_input(self.min_cell_count_text_ctrl)  # type: str

        validated = True
        try:
            # min cell count must be a positive integer value
            min_cell_count_value = int(min_cell_count_str)
            if min_cell_count_value <= 0:
                validated = False
        except ValueError:
            validated = False

        self.display_text_control_validation(self.min_cell_count_text_ctrl, validated)
        return validated

    def validate_ep_gen_avg_cell_size(self) -> bool:
        """
        Validates the user input to avg_cell_size_text_ctrl
        :return: Return True if the validation was successful. Return False otherwise.
        """
        avg_cell_size_str = self.str_from_text_input(self.avg_cell_size_text_ctrl)  # type: str

        try:
            # cell size must be a positive floating point value
            avg_cell_size_value = float(avg_cell_size_str)
            validated = avg_cell_size_value > 0
        except ValueError:
            validated = False

        self.display_text_control_validation(self.avg_cell_size_text_ctrl, validated)
        return validated

    def validate_ep_gen_cell_size_variance(self) -> bool:
        """
        Validates the user input to cell_size_variance_text_ctrl
        :return: Return True if the validation was successful. Return False otherwise.
        """
        variance_str = self.str_from_text_input(self.cell_size_variance_text_ctrl)

        try:
            # variance must be a floating point value
            variance_value = float(variance_str)
            # variance must not be greater than the average cell size
            if self.validate_ep_gen_avg_cell_size():
                avg_size = float(self.str_from_text_input(self.avg_cell_size_text_ctrl))
                validated = variance_value < avg_size
            else:
                # variance cannot be validated if there is an invalid average cell size
                validated = False
        except Exception:
            validated = False

        self.display_text_control_validation(self.cell_size_variance_text_ctrl, validated)
        return validated

    def validate_ep_gen_furrow_velocity(self) -> bool:
        """
        Validates the user input to furrow_velocity_text_ctrl
        :return: Return True if the validation was successful. Return False otherwise.
        """
        velocity_str = self.str_from_text_input(self.furrow_velocity_text_ctrl)

        try:
            # value must be non-zero positive float
            velocity = float(velocity_str)
            validated = velocity > 0
        except Exception:
            validated = False

        self.display_text_control_validation(self.furrow_velocity_text_ctrl, validated)
        return validated

    def validate_ep_gen_cell_max_size(self) -> bool:
        """
        Validates the user input to cell_max_size_text_ctrl
        :return: Return True if the validation was successful. Return False otherwise.
        """

        max_size_str = self.str_from_text_input(self.cell_max_size_text_ctrl)

        try:
            max_size = float(max_size_str)
            validated = max_size > 0
        except Exception:
            validated = False

        self.display_text_control_validation(self.cell_max_size_text_ctrl, validated)
        return validated

    def validate_ep_gen_cell_growth_rate(self) -> bool:
        """
        Validates the user input to cell_growth_rate_text_ctrl
        :return: Return True if the validation was successful. Return False otherwise.
        """

        cell_growth_rate_str = self.str_from_text_input(self.cell_growth_rate_text_ctrl)

        try:
            growth_rate = float(cell_growth_rate_str)
            validated = growth_rate >= 0
        except Exception:
            validated = False

        self.display_text_control_validation(self.cell_growth_rate_text_ctrl, validated)
        return validated

    def validate_simulation_speed(self) -> bool:
        """
        Validates the user input to simulation_speed_text_ctrl
        :return: Return True if the validation was successful. Return False otherwise.
        """

        simulation_speed_str = self.str_from_text_input(self.simulation_speed_text_ctrl)
        try:
            simulation_speed = float(simulation_speed_str)
            validated = simulation_speed > 0
        except Exception:
            validated = False

        self.display_text_control_validation(self.simulation_speed_text_ctrl, validated)
        return validated


    @staticmethod
    def display_text_control_validation(txt_control: TextCtrl, validated: bool = True) -> None:
        """
        Visualy displays the validation state of a text control
        Controls that have failed validation are displayed red. Controls that have not are displayed
        normally.
        :param txt_control: The validated text control.
        :param validated: The state of the controls validation. True for successful validation.
        False for unsuccessful validation.
        """
        if validated:
            txt_control.SetBackgroundColour(wx.NullColour)
        else:
            txt_control.SetBackgroundColour("Red")
        txt_control.Refresh()

    # endregion input validation

    # region simulation

    @ property
    def active_epithelium(self) -> Epithelium:
        """returns the active epithelium"""
        return self.__active_epithelium

    @ active_epithelium.setter
    def active_epithelium(self, value: Epithelium) -> None:
        """
        Sets the active epithelium and sets the epithelium for
        all listeners. A newly assigned epithelium is always considered to never have simulated.
        A newly assigned epithelium does not begin simulation right away.
        :param value: The new active epithelium
        :return: None
        """
        self.__active_epithelium = value
        self.has_simulated = False
        self.simulating = False
        self.active_epithelium.furrow.events = furrow_event_list

        # notify listeners of change
        for listener in self.epithelium_listeners:
            listener.epithelium = self.__active_epithelium

    def update_epithelium(self, event: wx.EVT_TIMER):
        """Simulates the active epithelium for one tick.
        Draws the updated epithelium."""
        self.active_epithelium.update()
        event.Skip(False)

        for listener in self.epithelium_listeners:
            listener.draw()

    @ property
    def simulating(self) -> bool:
        """Returns true if the active epithelium is being simulated. Returns false otherwise."""
        return self._simulating

    @ simulating.setter
    def simulating(self, simulate: bool) -> None:
        """
        Begins or ends the simulation of the active epithelium.
        :param simulate: begins simulation if true. Ends simulation otherwise.
        :return: None
        """

        # save the epithelium to a temporary location before it is simulated for the first time
        # this is used to reload the origonal state of the epithelium when simulation is stopped
        if simulate and not self.has_simulated:
            export_epithelium(self.active_epithelium, self.temporary_epithelium_location)

        self._simulating = simulate
        if simulate and len(self.active_epithelium.cells):
            frames_per_second = float(self.str_from_text_input(self.simulation_speed_text_ctrl))
            simulation_delay = 1000 / frames_per_second  # (MS per S) / fps = ms per update
            self.simulation_timer.Start(simulation_delay)
            self.has_simulated = True
        else:
            self.simulation_timer.Stop()

        self.update_enabled_widgets()

    @property
    def has_simulated(self):
        return self._has_simulated

    @ has_simulated.setter
    def has_simulated(self, value: bool):
        """true if the active epithelium has begn simulation. False Otherwise."""
        self._has_simulated = value
        self.update_enabled_widgets()

    # endregion simulation

    # region enable disable

    def update_enabled_widgets(self):
        """
        Enables or disables all input widgets based on application state.
        """

        # status bar updates:
        if self.generating_epithelium:
            self.status_bar.SetStatusText("Generating Epithelium...")
        else:
            self.status_bar.SetStatusText("")

        # Epithelium Creation
        self.ep_gen_create_button.Enable(not self.generating_epithelium)

        # epithelium file options
        enable_epithelium_file_options = not self.generating_epithelium
        self.ep_gen_save_button.Enable(enable_epithelium_file_options)
        self.ep_gen_save_as_button.Enable(enable_epithelium_file_options)
        self.ep_gen_load_button.Enable(enable_epithelium_file_options)

        # simulation settings file options
        enable_simulation_file_options = not self.generating_epithelium and not self.simulating
        self.m_sim_overview_save_button.Enable(enable_simulation_file_options)
        self.m_sim_overview_save_as_button.Enable(enable_simulation_file_options)
        self.m_sim_overview_load_button.Enable(enable_simulation_file_options)

        # simulation options
        self.enable_edit_simulation_options(not self.has_simulated and not self.generating_epithelium)
        self.enable_edit_specialization_options(not self.has_simulated and not self.generating_epithelium)

        # update status of simulation start stop and pause buttons
        for controller in self.simulation_controllers:
            start_button = controller.m_button4  # type: Button
            start_button.Enable(self.simulation_controllers_inputs_valid
                                and not self.generating_epithelium
                                and not self.simulating)
            pause_button = controller.m_button5
            pause_button.Enable(not self.generating_epithelium and self.has_simulated and self.simulating)
            stop_button = controller.m_button6
            stop_button.Enable(not self.generating_epithelium and self.has_simulated)

    def enable_edit_simulation_options(self, enable: bool):
        """Enables or disables user ability to edit all simulation options"""

        for option in self.m_sim_overview_sim_options_scrolled_window.GetChildren():
            if type(option) is not StaticText:
                option.Enable(enable)

    def enable_edit_specialization_options(self, enable: bool):
        """Enables or disables user ability to edit all specialization options"""

        for option in self.m_sim_overview_spec_options_scrolled_window.GetChildren():
            if type(option) is not StaticText:
                option.Enable(enable)

    # endregion enable disable

    # region misc

    @staticmethod
    def str_from_text_input(txt_control: TextCtrl):
        """
        Returns the string contained by a passed text control.
        :param txt_control: The contents of this TextCtrl will be returned.
        :return: The complete contents of the passed TextCtrl.
        """
        string_value = ''
        for i in range(txt_control.GetNumberOfLines()):
            string_value += txt_control.GetLineText(i)
        return string_value

    def update_gui_to_active_epithelium(self):
        """
        Updates all gui values to match the values stored by the active epithelium
        """

        epithelium = self.active_epithelium
        min_cell_count = len(epithelium.cells)
        if min_cell_count:
            average_cell_size = sum(map(lambda cell: cell.radius, epithelium.cells))/min_cell_count
        else:
            average_cell_size = 0
        cell_size_variance = max(map(lambda cell: abs(cell.radius-average_cell_size), epithelium.cells))

        self.min_cell_count_text_ctrl.SetValue(str(min_cell_count))
        self.avg_cell_size_text_ctrl.SetValue(str(average_cell_size))
        self.cell_size_variance_text_ctrl.SetValue(str(cell_size_variance))

    def update_epithelium_with_sim_options(self):
        """
        Updates the active epithelium with the simulation options from the GUI
        """

        if self.sim_overview_input_validation() and not self.has_simulated:
            # cell max size
            cell_max_size_str = self.str_from_text_input(self.cell_max_size_text_ctrl)  # type: str
            cell_max_size = float(cell_max_size_str)

            # cell growth rate
            cell_growth_rate_str = self.str_from_text_input(self.cell_growth_rate_text_ctrl)  # type: str
            cell_growth_rate = float(cell_growth_rate_str)

            # update cells
            for cell in self.active_epithelium.cells:
                cell.growth_rate = cell_growth_rate
                cell.max_radius = cell_max_size

            # set furrow velocity
            furrow_velocity_str = self.str_from_text_input(self.furrow_velocity_text_ctrl)
            furrow_velocity = float(furrow_velocity_str)
            self.active_epithelium.furrow.velocity = furrow_velocity

    def init_icon(self):
        """initializes and displays the application icon."""
        image = wx.Image(r"./resources/EDM-1.png")  # type: wx.Image
        bitmap = image.ConvertToBitmap()  # type: wx.Bitmap
        icon = wx.Icon()  # type: wx.Icon
        icon.CopyFromBitmap(bitmap)
        self.SetIcon(icon)

    # endregion misc
