class NotEnoughProductUnits(Exception):
    """ Exception raised for errors related to updating product units.
        Most possibly related to inventory movement operations

    Attributes:
        message -- Error details
    """

    def __init__(self, message="Not enough units available on product to perform the requested operation"):
        self.message = message
        super().__init__(self.message)
