import helpers
import sympy


def test_euclidian_distance():
    assert(helpers.euclidian_distance([1], [-1]) == 2)
    assert(helpers.euclidian_distance([1,2], [0,0]) == sympy.sqrt(5))
    assert(helpers.euclidian_distance([1], [1, 2]) == -1)
    assert(helpers.euclidian_distance([], []) == 0)
