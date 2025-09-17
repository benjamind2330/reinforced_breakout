from .vec2 import vec2

class aabb:
    def __init__(self, min_point: vec2, max_point: vec2):
        self.min = min_point
        self.max = max_point

    def __repr__(self):
        return f"aabb(min={self.min}, max={self.max})"

    def closest_point(self, point: vec2) -> vec2:
        """Return the closest point on the AABB to the given point."""
        clamped_x = max(self.min.x, min(point.x, self.max.x))
        clamped_y = max(self.min.y, min(point.y, self.max.y))
        return vec2(clamped_x, clamped_y)
    
    def closest_side(self, point: vec2) -> vec2:
        """Return a normal representing the side of the AABB closest to the given point. The normal points outwards from the aabb."""
        distances = {
            'left': abs(point.x - self.min.x),
            'right': abs(point.x - self.max.x),
            'top': abs(point.y - self.min.y),
            'bottom': abs(point.y - self.max.y)
        }
        closest_side = min(distances, key=distances.get)
        if closest_side == 'left':
            return vec2(-1, 0)
        elif closest_side == 'right':
            return vec2(1, 0)
        elif closest_side == 'top':
            return vec2(0, -1)
        elif closest_side == 'bottom':
            return vec2(0, 1)

