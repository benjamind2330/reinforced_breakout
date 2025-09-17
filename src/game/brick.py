from physics.aabb import aabb
from physics.vec2 import vec2

class brick:
    def __init__(self, position: aabb):
        self.position = position
        self.alive = True

    def hit(self, point: vec2):
        self.alive = False
        return self.position.closest_side(point)
        

    def __repr__(self):
        return f"brick(position={self.position}, hits={self.hits}, alive={self.alive})"