from physics.aabb import aabb
from physics.vec2 import vec2

class brick:
    def __init__(self, box: aabb):
        self.box = box
        self.alive = True

    def hit(self, point: vec2):
        self.alive = False
        return self.box.closest_side(point)
        

    def __repr__(self):
        return f"brick(box={self.box}, alive={self.alive})"