import queue


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
                 event_queue: queue.Queue = None) -> None:
        """Initialize this instance of Furrow.
        :param position: The horizontal position of this Furrow.
        :param width: The width of the furrows immediate effect.
        :param velocity: how many units the furrow moves in one 'tick'.
        :param event_queue: Events (stored as callable objects) triggered by the progression of the furrow.
        """
        self.position = position  # type: float
        self.width = width  # type: float
        self.velocity = velocity  # type: float
        self.event_queue = event_queue  # type: queue.Queue

        if self.event_queue is None:
            self.event_queue = queue.Queue()

    def advance(self, distance: float = 0) -> None:
        """
        Moves the furrow forward by the specified amount.
        :param distance: how far to move this Furrow
        """
        self.position += distance

    def update(self):
        """
        Simulates this Furrow for one tick.
        """

        # move the furrow forward
        self.advance(self.velocity)
