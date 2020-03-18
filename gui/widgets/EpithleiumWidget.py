from PyQt5 import QtGui

from .PanTool import PanTool
from .qtmoderngl import QModernGLWidget
from display_2d import EpitheliumScene
from epithelium_backend import Epithelium


class EpitheliumWidget(QModernGLWidget):
    """A custom ModernGL widget to display an EpitheliumScene."""

    # Class pan tool for all EpitheliumWidgets to share to stay synced
    _pan_tool = PanTool()

    def __init__(self, *args):
        super().__init__()

        self.ctx = None
        self.scene = None

    @property
    def width(self) -> int:
        return super().width() * self.devicePixelRatio()

    @property
    def height(self) -> int:
        return super().height() * self.devicePixelRatio()

    @property
    def epithelium(self) -> Epithelium:
        return self.scene.epithelium

    @epithelium.setter
    def epithelium(self, epithelium):
        self.scene.epithelium = epithelium
        self.update()

    def init(self):
        self.ctx.viewport = (0, 0, self.width, self.height)
        self.scene = EpitheliumScene(self.ctx)
        self.update()

    def render(self):
        self.screen.use()
        self.scene.clear()
        self.scene.draw()

    def resizeEvent(self, event: QtGui.QResizeEvent):
        if self.ctx:
            # Adjust the context based on the new window size
            self.ctx.viewport = (0, 0, self.width, self.height)
            self.scene.resize(self.ctx)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        EpitheliumWidget._pan_tool.start_drag(event.x() / self.width, event.y() / self.height)
        self.scene.pan(*EpitheliumWidget._pan_tool.value)
        self.update()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        EpitheliumWidget._pan_tool.dragging(event.x() / self.width, event.y() / self.height)
        self.scene.pan(*EpitheliumWidget._pan_tool.value)
        self.update()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        EpitheliumWidget._pan_tool.stop_drag(event.x() / self.width, event.y() / self.height)
        self.scene.pan(*EpitheliumWidget._pan_tool.value)
        self.update()

    def wheelEvent(self, event: QtGui.QWheelEvent):
        rotation = event.angleDelta().y()

        # Certain systems have inverted scroll values (natural scroll on macOS)
        if event.inverted():
            rotation *= -1

        self.scene.zoom(rotation)
        self.update()
