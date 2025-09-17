

class vec2:
    def __init__(self, x: float=0.0, y: float=0.0):
        self.x = x
        self.y = y

    def __add__(self, other: 'vec2') -> 'vec2':
        return vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'vec2') -> 'vec2':
        return vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> 'vec2':
        return vec2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float) -> 'vec2':
        return vec2(self.x / scalar, self.y / scalar)

    def dot(self, other: 'vec2') -> float:
        return self.x * other.x + self.y * other.y

    def length(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5

    def normalize(self) -> 'vec2':
        length = self.length()
        if length == 0:
            return vec2(0, 0)
        return self / length

    def __repr__(self):
        return f"vec2({self.x}, {self.y})"
