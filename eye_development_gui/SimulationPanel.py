from eye_development_gui.SimulationPanelBase import SimulationPanelBase
from epithelium_backend.Epithelium import Epithelium
# Implementing SimulationPanel


class SimulationPanel(SimulationPanelBase):
    """Displays a simulated epithelium and provides the ability
    to start, stop, and pause simulation of the epithelium"""

    def __init__(self, parent, _id, pos, _size, style):
        """Initializes the SimulationPanel
        :param parent: The parent of this panel
        :param _id: ignored, but required for wxFormBuilder
        :param pos: ignored, but required for wxFormBuilder
        :param _size: ignored, but required for wxFormBuilder
        :param style: ignored, but required for wxFormBuilder
        """
        SimulationPanelBase.__init__(self, parent)
        self.simulation_listeners = []

    @property
    def epithelium(self) -> Epithelium:
        """returns the epithelium that is being displayed"""
        return self.m_epithelium_display.epithelium

    @epithelium.setter
    def epithelium(self, value: Epithelium):
        """Sets the epithelium that is to be displayed
        :param value: New epithelium to be displayed
        """
        self.m_epithelium_display.epithelium = value

    def start_simulation_callback(self, event):
        """ Callback invoked when the SimulationPanel's 'start' button is pressed.
        Signals all listeners to begin simulating."""
        for listener in self.simulation_listeners:
            listener.update_epithelium_with_sim_options()
            listener.simulating = True
        event.Skip(False)

    def stop_simulation_callback(self, event):
        """ Callback invoked when the SimulationPanel's 'stop' button is pressed.
            Signals all listeners to stop simulating."""
        for listener in self.simulation_listeners:
            listener.simulating = False
        event.Skip(False)

    def draw(self):
        """Forces a draw on the contained OpenGL Canvas"""
        self.m_epithelium_display.draw()
