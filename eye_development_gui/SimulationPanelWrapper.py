"""Subclass of SimulationPanel, which is generated by wxFormBuilder."""

from eye_development_gui.SimulationPanelBase import SimulationPanel

# Implementing SimulationPanel
class SimulationPanelWrapper( SimulationPanel ):
	def __init__( self, parent, a, b, c, d):
		SimulationPanel.__init__( self, parent )
	