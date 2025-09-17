import math
import pytest
from physics.vec2 import vec2

# filepath: reinforced_breakout/tests/test_physics_tests.py
# We recommend installing an extension to run python tests.



def test_addition():
    a = vec2(1.5, -2.0)
    b = vec2(-0.5, 4.0)
    c = a + b
    assert c.x == pytest.approx(1.0)
    assert c.y == pytest.approx(2.0)


def test_subtraction():
    a = vec2(5.0, 3.0)
    b = vec2(2.0, 7.0)
    c = a - b
    assert c.x == pytest.approx(3.0)
    assert c.y == pytest.approx(-4.0)


def test_scalar_multiplication():
    a = vec2(3.0, -4.0)
    c = a * 2
    assert c.x == pytest.approx(6.0)
    assert c.y == pytest.approx(-8.0)


def test_scalar_division():
    a = vec2(8.0, -6.0)
    c = a / 2
    assert c.x == pytest.approx(4.0)
    assert c.y == pytest.approx(-3.0)


def test_dot_product():
    a = vec2(3.0, 4.0)
    b = vec2(-2.0, 5.0)
    assert a.dot(b) == pytest.approx(3 * -2 + 4 * 5)  # -6 + 20 = 14


def test_length():
    a = vec2(3.0, 4.0)
    assert a.length() == pytest.approx(5.0)


def test_normalize_non_zero():
    a = vec2(10.0, 0.0)
    n = a.normalize()
    assert n.x == pytest.approx(1.0)
    assert n.y == pytest.approx(0.0)
    assert n.length() == pytest.approx(1.0)


def test_normalize_diagonal():
    a = vec2(5.0, 5.0)
    n = a.normalize()
    expected = 1 / math.sqrt(2)
    assert n.x == pytest.approx(expected)
    assert n.y == pytest.approx(expected)
    assert n.length() == pytest.approx(1.0)


def test_normalize_zero_vector():
    a = vec2(0.0, 0.0)
    n = a.normalize()
    assert n.x == 0.0
    assert n.y == 0.0
    assert n.length() == 0.0


def test_chained_operations():
    a = vec2(1.0, 2.0)
    b = vec2(3.0, 4.0)
    c = ((a + b) * 2 - b) / 2
    # (a + b) = (4,6); *2 -> (8,12); -b -> (5,8); /2 -> (2.5,4)
    assert c.x == pytest.approx(2.5)
    assert c.y == pytest.approx(4.0)


def test_repr():
    a = vec2(1.25, -3.5)
    r = repr(a)
    assert "vec2" in r
    assert "1.25" in r
    assert "-3.5" in r


@pytest.mark.parametrize(
    "x,y,scalar",
    [
        (0.0, 0.0, 5),
        (2.2, -3.3, -1),
        (-5.5, 4.4, 0.5),
        (1e6, -1e6, 1e-6),
    ],
)
def test_round_trip_scale_divide(x, y, scalar):
    v = vec2(x, y)
    scaled = v * scalar
    round_trip = scaled / scalar
    assert round_trip.x == pytest.approx(v.x)
    assert round_trip.y == pytest.approx(v.y)


def test_dot_with_normalized_is_projection_length_times_length():
    a = vec2(3.0, 4.0)      # length 5
    b = vec2(5.0, 0.0)      # along x
    n_b = b.normalize()     # (1,0)
    projection = a.dot(n_b) # should be a.x = 3
    assert projection == pytest.approx(3.0)
