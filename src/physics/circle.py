from .vec2 import vec2

class circle:
    def __init__(self, center: vec2, radius: float):
        self.center = center
        self.radius = radius

    def __repr__(self):
        return f"circle(center={self.center}, radius={self.radius})"