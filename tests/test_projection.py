import pytest

from fdf.model import Map, Point
from fdf.projection import Camera, height_color, lerp_color


def test_projection_origin() -> None:
    camera = Camera()
    point = Point(0, 0, 0)
    assert camera.project(point) == (0.0, 0.0)


def test_projection_height_is_negative() -> None:
    camera = Camera(z_scale=1.0)
    projected = camera.project(Point(0, 0, 1))
    assert projected[1] < 0


def test_isometric_projection_uses_expected_axes() -> None:
    camera = Camera()
    assert camera.project(Point(1, 0, 0)) == pytest.approx((0.8660254037844386, 0.5))
    assert camera.project(Point(0, 1, 0)) == pytest.approx((-0.8660254037844386, 0.5))


def test_top_view_uses_xy_and_ignores_height() -> None:
    camera = Camera()
    camera.top_view = True
    assert camera.project(Point(3, 4, 20)) == (3.0, 4.0)


def test_top_view_can_rotate_without_using_height() -> None:
    camera = Camera(angle=90.0)
    camera.top_view = True
    assert camera.project(Point(1, 0, 100)) == pytest.approx((0.0, 1.0))


def test_vertical_rotation_rotates_map_in_xy_plane() -> None:
    camera = Camera(angle=90.0, z_scale=1.0)
    projected = camera.project(Point(1, 0, 0))
    assert projected[0] != 0.0
    assert projected[1] != 0.0


def test_pan_moves_projected_points() -> None:
    camera = Camera()
    point = Point(1, 2, 0)
    before = camera.project(point)
    camera.pan(12, -8)
    after = camera.project(point)
    assert after == (before[0] + 12, before[1] - 8)


def test_zoom_keeps_anchor_fixed() -> None:
    camera = Camera()
    camera.fit(Map([[Point(0, 0, 0), Point(2, 0, 1)], [Point(0, 2, 0), Point(2, 2, 0)]]), 800, 600)
    point = Point(1, 1, 0)
    anchor = camera.project(point)
    camera.zoom(2.0, *anchor)
    assert camera.scale == camera._fit_scale * 2.0
    assert camera.project(point) == pytest.approx(anchor)


def test_camera_fit_keeps_points_in_window() -> None:
    data = Map([
        [Point(0, 0, 0), Point(1, 0, 0), Point(2, 0, 0)],
        [Point(0, 1, 0), Point(1, 1, 0), Point(2, 1, 0)],
    ])
    camera = Camera()
    camera.fit(data, 800, 600)
    points = [camera.project(point) for point in data]
    xs = [x for x, _ in points]
    ys = [y for _, y in points]
    assert min(xs) >= 0 and max(xs) <= 800
    assert min(ys) >= 0 and max(ys) <= 600


def test_color_interpolation() -> None:
    assert lerp_color("#000000", "#FFFFFF", 0.5) == "#7F7F7F"
    assert height_color(0, 0, 10) == "#1B6DFF"
    assert height_color(10, 0, 10) == "#FF4D4D"
