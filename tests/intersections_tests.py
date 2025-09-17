
import pytest

# Import modules under test (absolute import, not relative)
from physics.circle import circle  # noqa: E402
from physics.aabb import aabb  # noqa: E402
from physics.intersections import intersects  # noqa: E402
from physics.vec2 import vec2  # noqa: E402

def make_aabb(xmin, ymin, xmax, ymax):
    return aabb(vec2(xmin, ymin), vec2(xmax, ymax))

def make_circle(cx, cy, r):
    return circle(vec2(cx, cy), r)


def test_circle_inside_aabb():
    box = make_aabb(-2, -2, 2, 2)
    circ = make_circle(0, 0, 1)
    assert intersects(circ, box) is True
    assert intersects(box, circ) is True

def test_circle_tangent_returns_false_due_to_strict_comparison():
    # circle centered at (2,0) radius 1 touching aabb max.x=1 edge: distance^2 == radius^2
    box = make_aabb(-1, -1, 1, 1)
    circ_tangent = make_circle(2, 0, 1)
    assert intersects(circ_tangent, box) is False
    assert intersects(box, circ_tangent) is False

def test_circle_just_inside_edge_returns_true():
    box = make_aabb(-1, -1, 1, 1)
    circ_inside = make_circle(1.99, 0, 1)  # distance_x = 0.99 -> inside
    assert intersects(circ_inside, box) is True
    assert intersects(box, circ_inside) is True

@pytest.mark.parametrize(
    "circ,box,expected",
    [
        (make_circle(0, 0, 0.5), make_aabb(-1, -1, 1, 1), True),
        (make_circle(3, 3, 0.5), make_aabb(-1, -1, 1, 1), False),
        (make_circle(1.5, 0, 1), make_aabb(-1, -1, 1, 1), True),   # overlaps beyond right edge
        (make_circle(-1.5, 0, 0.4), make_aabb(-1, -1, 1, 1), False),
    ]
)
def test_various_circle_aabb_cases(circ, box, expected):
    assert intersects(circ, box) is expected
    assert intersects(box, circ) is expected