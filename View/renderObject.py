class RenderObject:
    """
    Class for rendering special object.
    """
    def __init__(self, pos, time, immortal = True):
        self.pos = pos
        self.time = time
        self.totaltime = time
        self.immortal = immortal

    def update(self):
        self.time -= 1

class Explosion(RenderObject):
    """
    Class for rendering the explosion effect.
    """
    def __init__(self, index, pos, radius, time):
        super().__init__(pos, time, False)
        self.index = index
        self.radius = radius

class TimeLimitExceedStamp(RenderObject):
    """
    Class for censuring the dilatory mischiefs.
    """
    def __init__(self, pos, time):
        super().__init__(pos, time)

class MagicCircle(RenderObject):
    """
    Class for summon the Dark Bullet Death Deity.
    """
    def __init__(self, pos, time):
        super().__init__(pos, time)
        self.theta = 0.0

    def update(self):
        super().update()
        self.theta += 180 / self.totaltime if self.time > 0 else 0.1

class CountDown(RenderObject):
    """
    Class for count down.
    """
    def __init__(self, pos, time):
        super().__init__(pos, time, False)

class MovingScore(RenderObject):
    def __init__(self, index, pos, time):
        super().__init__(pos, time)
        self.index = index
