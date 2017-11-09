import wx
from eye_development_gui.eye_development_gui import MainFrame

if __name__ == '__main__':
    # Run the app
    app = wx.App()  # type: wx.App
    frame = MainFrame(None)
    frame.Show(True)
    app.MainLoop()