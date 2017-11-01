from epithelium_backend.Cell import Cell

class Furrow:
    """
    Simulates a morphogenetic furrow. Stores and maintains all information related to the
    morphogenetic furrow (movement speed, position, etc...). Used to apply a sequence of development
    events to an Epithelium.
    """

    def __init__(self,
                 position: float = 0,
                 width: float = 1,
                 velocity: float = 0,
                 events: list = None) -> None:
        """Initialize this instance of Furrow.
        :param position: The horizontal position of this Furrow.
        :param width: The width of the furrows immediate effect.
        :param velocity: how many units the furrow moves in one 'tick'.
        :param events: Specialization events (stored as callable objects) triggered by the progression of the furrow.
        """
        self.position = position  # type: float
        self.width = width  # type: float
        self.velocity = velocity  # type: float
        self.events = events  # type: list

        if self.events is None:
            self.events = []

    def advance(self, distance: float = 0) -> None:
        """
        Moves the furrow forward by the specified amount.
        :param distance: how far to move this Furrow
        """
        self.position += distance

    def update(self, cells: Cell) -> None:
        """
        Simulates this Furrow for one tick.
        :param cells: The cells that will be impacted by this update.
        """

        # move the furrow forward
        self.advance(self.velocity)

        # run events on the cells
        for event in self.events:
            event(cells)
