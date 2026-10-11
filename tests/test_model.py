from fdf.model import Map, Point


def test_map_len_and_iteration() -> None:
    grid = [
        [Point(0, 0, 0), Point(1, 0, 1)],
        [Point(0, 1, 2), Point(1, 1, 3)],
    ]
    mapped = Map(grid)
    assert len(mapped) == 4
    values = [point.z for point in mapped]
    assert values == [0, 1, 2, 3]


def test_neighbors_for_corner() -> None:
    grid = [[Point(0, 0, 0), Point(1, 0, 1)], [Point(0, 1, 2), Point(1, 1, 3)]]
    mapped = Map(grid)
    neighbors = mapped.neighbors(0, 0)
    assert len(neighbors) == 2
    assert {neighbor.x for neighbor in neighbors} == {1, 0}
