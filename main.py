from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
import sys

from gui import Window

app = QtWidgets.QApplication(sys.argv)
app.setWindowIcon(QIcon("gui/resources/icon.png"))
window = Window()
window.show()
sys.exit(app.exec_())
