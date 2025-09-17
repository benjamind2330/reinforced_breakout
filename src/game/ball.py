from physics.circle import circle
from physics.vec2 import vec2

class ball:
    def __init__(self, position: vec2, velocity: vec2, radius: float):
        self.position = position
        self.velocity = velocity
        self.radius = radius
        self.shape = circle(center=position, radius=radius)
    
    def update(self, dt: float):
        self.position += self.velocity * dt
        self.shape.center = self.position
    
    def bounce(self, normal: vec2):
        self.velocity = self.velocity - normal * (2 * self.velocity.dot(normal))

    def __repr__(self):
        return f"ball(position={self.position}, velocity={self.velocity}, radius={self.radius})"
    
