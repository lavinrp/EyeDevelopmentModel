
class Furrow:
    """
    Simulates a morphogenetic furrow. Stores and maintains all information related to the
    morphogenetic furrow (movement speed, position, etc...). Used to apply a sequence of development
    events to an Epithelium.
    """

    def __init__(self, position: float = 0, width: float = 1, velocity: float = 0) -> None:
        """Initialize this instance of Furrow
        :param position: The horizontal position of this Furrow
        :param width: The width of the furrows immediate effect
        :param velocity: how many units the furrow moves in one 'tick'
        """
        self.position = position  # type: float
        self.width = width  # type: float
        self.velocity = velocity  # type: float
