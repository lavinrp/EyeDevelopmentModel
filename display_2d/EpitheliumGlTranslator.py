from epithelium_backend.Epithelium import Epithelium
import numpy

class EpitheliumGlTranslator:
    """Translates the epithelium into data that can be displayed via OpenGL"""

    def __init__(self, epithelium: Epithelium = None) -> None:
        """
        Initializes this instance of EpitheliumGlTranslator.
        :param epithelium: The epithelium to be translated. Defaults to None.
        """
        self.epithelium=epithelium  # type: Epithelium

    def get_cell_centers(self) -> numpy.ndarray:
        """Returns a numpy array containing the center possition of each cell"""
        # TODO: add error checking for epithelium or epithelium.cells being None??

        # gather the positions of each cell
        positions_list = []
        for cell in self.epithelium.cells:
            positions_list.append(cell.position)

        # convert to numpy array and return
        return numpy.array(positions_list, dtype=numpy.float32)
