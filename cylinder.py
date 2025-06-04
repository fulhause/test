class Cylinder:
    """Simple cylinder model supporting 2-position and 3-position modes."""

    POS_RETRACTED = "retracted"
    POS_EXTENDED = "extended"
    POS_INTERMEDIATE = "intermediate"

    def __init__(self, mode="2-position"):
        if mode not in {"2-position", "3-position"}:
            raise ValueError("mode must be '2-position' or '3-position'")
        self.mode = mode
        self.position = self.POS_RETRACTED

    def extend(self):
        self.position = self.POS_EXTENDED

    def retract(self):
        self.position = self.POS_RETRACTED

    def intermediate(self):
        if self.mode != "3-position":
            raise ValueError("intermediate position only valid in 3-position mode")
        self.position = self.POS_INTERMEDIATE

    def get_position_signals(self):
        signals = {
            self.POS_RETRACTED: False,
            self.POS_EXTENDED: False,
            self.POS_INTERMEDIATE: False,
        }
        signals[self.position] = True
        if self.mode == "2-position":
            signals.pop(self.POS_INTERMEDIATE)
        return signals
