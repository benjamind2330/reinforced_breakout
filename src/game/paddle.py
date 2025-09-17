from physics.aabb import aabb

class paddle:
    def __init__(self, position: aabb):
        self.position = position

    def move(self, delta_x: float):
        self.position.min.x += delta_x
        self.position.max.x += delta_x

    def __repr__(self):
        return f"paddle(position={self.position})"