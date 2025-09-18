from physics.aabb import aabb
from physics.vec2 import vec2
from utility.math import clamp

class paddle:
    def __init__(self, position: vec2, length: float, height: float):
        self.position = position
        self.length = length
        self.height = height

    def move(self, delta_x: float, bounds: vec2):
        self.position.x += delta_x
        self.position.x = clamp(self.position.x, bounds.x + self.length / 2, bounds.y - self.length / 2)

    def aabb(self) -> aabb:
        return aabb(min=vec2(self.position.x - self.length / 2, self.position.y - self.height / 2), max=vec2(self.position.x + self.length / 2, self.position.y + self.height / 2))

    def __repr__(self):
        return f"paddle(position={self.position}, length={self.length}, height={self.height})"