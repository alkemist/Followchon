from src.models.classes.guinea_pig import GuineaPig


class Stitch(GuineaPig):
    cls = 3
    name = 'Plate'

    def __init__(self):
        super().__init__()
