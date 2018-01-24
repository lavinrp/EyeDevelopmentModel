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
        # Just for the demo.
        self.m_epithelium_display._epithelium.go()
