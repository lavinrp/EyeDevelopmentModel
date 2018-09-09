import sys

from PySide2 import QtWidgets

from eye_development_gui_pyside.MainWidget import MainWidget


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)


    widget = MainWidget()

    widget.show()


    sys.exit(app.exec_())