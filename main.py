import sys

from PySide2 import QtWidgets

from eye_development_gui_pyside.MainWidget import MainWidget
from eye_development_gui_pyside.EpitheliumGenerationWidget import EpitheliumGenerationWidget


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)


    widget = MainWidget()
    # widget = EpitheliumGenerationWidget()

    widget.show()


    sys.exit(app.exec_())