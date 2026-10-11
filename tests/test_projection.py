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
