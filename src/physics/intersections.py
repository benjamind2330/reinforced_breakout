from .circle import circle
from .aabb import aabb
from functools import singledispatch


@singledispatch
def intersects(a, b) -> bool:
    raise NotImplementedError(f"Intersection not implemented for types {type(a)} and {type(b)}")

@intersects.register
def _(a: circle, b: aabb) -> bool:
    closest = b.closest_point(a.center)
    distance_x = a.center.x - closest.x
    distance_y = a.center.y - closest.y
    return (distance_x**2 + distance_y**2) < (a.radius**2) or b.contains(a.center)

@intersects.register
def _(a: aabb, b: circle) -> bool:
    return intersects(b, a)