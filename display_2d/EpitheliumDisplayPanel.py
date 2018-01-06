import wx
from wx import glcanvas

from OpenGL.GL import *
from OpenGL.GLU import *

from epithelium_backend.Epithelium import Epithelium
from display_2d.GlDrawingPrimitives import draw_circle


class EpitheliumDisplayCanvas(glcanvas.GLCanvas):
    """OpenGL canvas used to display an epithelium"""
    def __init__(self, parent):
        # TODO: correctly set the size of EpitheliumDisplayCanvas
        glcanvas.GLCanvas.__init__(self, parent, size=(800, 800), name='epithelium_display_canvas')

        # GL
        self.context = None  # type: glcanvas.GLContext
        self.__gl_initialized = False  # type: bool
        self.__camera_x = 0  # type: float
        self.__camera_y = 0  # type: float
        self.__scale = 0.1  # type: float



        # event handling
        self.Bind(wx.EVT_PAINT, self.on_draw)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse_events)
        self.__panning = False  # type: bool
        self.__last_mouse_position = [0, 0]  # type: list

    def on_draw(self, e):
        # openGL setup
        if not self.__gl_initialized:

            # context setup
            self.context = glcanvas.GLContext(self)
            self.SetCurrent(self.context)

            # gl settings
            glViewport(0, 0, 800, 800)
            glLoadIdentity()
            glClearColor(.9, .9, .9, 1)
            glMatrixMode(GL_PROJECTION)
            gluLookAt(self.__camera_x, self.__camera_y, 1,  # eye
                      self.__camera_x, self.__camera_y, 0,  # target
                      0,                1,              0)  # up vector
            glScalef(self.__scale, self.__scale, 1)

            # finalize init
            self.__gl_initialized = True

        # draw
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        draw_circle((0, 0), 0.3, True, color=(0, 1, 0, 1))
        draw_circle((0.6, 0), 0.3, True, color=(0, 0, 1, 1))

        self.SwapBuffers()

    def on_mouse_events(self, event: wx.MouseEvent):
        """Handle all mouse event logic.
        This includes: camera panning
        :param event: the mouse event to handle
        """

        # get mouse position
        current_mouse_position = [event.GetX(), event.GetY()]

        # left mouse button down
        if event.ButtonDown(wx.MOUSE_BTN_LEFT):
            self.__panning = True

        # left mouse button up
        if event.ButtonUp(wx.MOUSE_BTN_LEFT):
            self.__panning = False

        if event.Dragging():
            #print("dragging at: " + str(event.GetX()) + "," + str(event.GetY()))

            # panning
            if self.__panning:
                self._pan_camera(self.__last_mouse_position[0] - current_mouse_position[0],
                                 self.__last_mouse_position[1] - current_mouse_position[1])

        # update mouse position
        self.__last_mouse_position = current_mouse_position

    def _pan_camera(self, delta_x: float, delta_y: float) -> None:
        """Pan the camera by the specified deltas
        :param delta_x: change in the x of the camera
        :param delta_y: change in the y of the camera
        """

        distance_modifier = 0.001  # type: float

        self.__camera_x += delta_x * distance_modifier
        self.__camera_y += delta_y * distance_modifier
        glMatrixMode(GL_PROJECTION)
        gluLookAt(self.__camera_x, self.__camera_y, 1,  # eye
                  self.__camera_x, self.__camera_y, 0,  # target
                  0, 1, 0)  # up vector
        print(str(self.__camera_x) + "," + str(self.__camera_y))
        self.on_draw(None)


class EpitheliumDisplayPanel(wx.Panel):
    """Panel For real-time drawing of an epithelium"""
    def __init__(self, parent, a, b, c, d) -> None:

        # init the panel
        super().__init__(parent, a, b, c, d)

        # create gl canvas
        self.gl_canvas = EpitheliumDisplayCanvas(self)

        # create default epithelium
        self.epithelium = Epithelium(5)  # type: Epithelium
