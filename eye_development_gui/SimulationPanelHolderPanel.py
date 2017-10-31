import wx
import wx.xrc



class SimulationPanelHolderPanel(wx.Panel):
    """Creates stores and displays a SimulationPanel. This is a hack to get SimulationPanel to display."""

    def __init__(self,  parent, id_=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 300),
                 style=wx.TAB_TRAVERSAL):

        wx.Panel.__init__(self, parent, id=id_, pos=pos, size=size, style=style)

        main_fg_sizer = wx.FlexGridSizer(0, 2, 0, 0)
        main_fg_sizer.SetFlexibleDirection(wx.BOTH)
        main_fg_sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_panel = None#eye_development_guiSimulationPanel(self)
        main_fg_sizer.Add(self.m_panel, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(main_fg_sizer)
        self.Layout()
