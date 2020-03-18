from PyQt5 import QtCore

from epithelium_backend.CellFactory import CellFactory
from epithelium_backend.Epithelium import Epithelium


class EpitheliumGenerator(QtCore.QThread):
    """Threaded generator to create epitheliums in the background."""

    epithelium_signal = QtCore.pyqtSignal(Epithelium)

    def __init__(self, min_cell_count, average_cell_size, cell_variance_size):
        super().__init__()

        self._min_cell_count = min_cell_count
        self._average_cell_size = average_cell_size
        self._cell_variance_size = cell_variance_size

    @QtCore.pyqtSlot()
    def generate_epithelium(self):
        """Creates a new epithelium to return to Window."""
        cell_factory = CellFactory()
        cell_factory.radius_divergence = self._cell_variance_size / self._average_cell_size
        cell_factory.average_radius = self._average_cell_size

        epithelium = Epithelium(cell_quantity=self._min_cell_count,
                                cell_avg_radius=self._average_cell_size,
                                cell_factory=cell_factory)

        self.epithelium_signal.emit(epithelium)
