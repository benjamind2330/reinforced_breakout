from .circle import circle
from .aabb import aabb
from functools import singledispatch


@singledispatch
def intersects(a, b) -> bool:
    raise NotImplementedError(f"Intersection not implemented for types {type(a)} and {type(b)}")

@intersects.register
def _(a: circle, b: aabb) -> bool:
    closest_x = max(b.min.x, min(a.center.x, b.max.x))
    closest_y = max(b.min.y, min(a.center.y, b.max.y))
    distance_x = a.center.x - closest_x
    distance_y = a.center.y - closest_y
    return (distance_x**2 + distance_y**2) < (a.radius**2)

@intersects.register
def _(a: aabb, b: circle) -> bool:
    return intersects(b, a)