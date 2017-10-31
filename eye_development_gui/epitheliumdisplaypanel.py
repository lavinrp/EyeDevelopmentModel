

import wx
import wx.xrc


class EpitheliumDisplayPanel(wx.Panel):
    def __init__(self, parent, id_, pos, size, style):
        wx.Panel.__init__(self, parent, id=id_, pos=pos, size=size,
                          style=style)

        fgSizer3 = wx.FlexGridSizer(2, 0, 0, 0)
        fgSizer3.AddGrowableCol(0)
        fgSizer3.AddGrowableRow(1)
        fgSizer3.SetFlexibleDirection(wx.BOTH)
        fgSizer3.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        bSizer7 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_bpButton1 = wx.BitmapButton(self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize,
                                           wx.BU_AUTODRAW)
        bSizer7.Add(self.m_bpButton1, 0, wx.ALL, 5)

        self.m_bpButton2 = wx.BitmapButton(self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize,
                                           wx.BU_AUTODRAW)
        bSizer7.Add(self.m_bpButton2, 0, wx.ALL, 5)

        self.m_bpButton3 = wx.BitmapButton(self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize,
                                           wx.BU_AUTODRAW)
        bSizer7.Add(self.m_bpButton3, 0, wx.ALL, 5)

        fgSizer3.Add(bSizer7, 1, wx.EXPAND, 5)

        self.m_panel5 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        fgSizer3.Add(self.m_panel5, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(fgSizer3)
        self.Layout()

    def __del__(self):
        pass