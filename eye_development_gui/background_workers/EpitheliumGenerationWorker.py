"""
Based on code from https://wiki.wxpython.org/Non-Blocking%20Gui
"""

import threading

import wx

from epithelium_backend.CellFactory import CellFactory
from epithelium_backend.Epithelium import Epithelium


_EVT_GENERATE_EPITHELIUM = wx.NewEventType()
EVT_GENERATE_EPITHELIUM = wx.PyEventBinder(_EVT_GENERATE_EPITHELIUM, 1)


class EpitheliumGenerationEvent(wx.PyCommandEvent):
    """Event to signal that an epithelium has been created."""

    def __init__(self, etype, eid, epithelium=None):
        """initialize the event"""
        wx.PyCommandEvent.__init__(self, etype, eid)
        self.epithelium = epithelium

    def get_epithelium(self) -> Epithelium:
        """Returns the epithelium tied to the event."""
        return self.epithelium


class EpitheliumGenerationWorker(threading.Thread):
    """
    Background worker that generates an epithelium in a background thread then returns.
    """

    def __init__(self,
                 parent,
                 min_cell_count,
                 avg_cell_size,
                 radius_divergence):
        """Initialize this background worker."""

        threading.Thread.__init__(self)

        self.parent = parent
        self.min_cell_count = min_cell_count
        self.avg_cell_size = avg_cell_size
        self.radius_divergence = radius_divergence
        self.cell_factory = CellFactory()
        self.cell_factory.radius_divergence = radius_divergence
        self.cell_factory.average_radius = avg_cell_size

    def run(self):
        """
        Creates an epithelium and sets it as the result of this worker.
        Overrides Thread.run. Called internally when thread.start() is invoked
        :return:
        """

        epithelium = Epithelium(cell_quantity=self.min_cell_count,
                                cell_avg_radius=self.avg_cell_size,
                                cell_factory=self.cell_factory)

        event = EpitheliumGenerationEvent(_EVT_GENERATE_EPITHELIUM, -1, epithelium)
        wx.PostEvent(self.parent, event)

